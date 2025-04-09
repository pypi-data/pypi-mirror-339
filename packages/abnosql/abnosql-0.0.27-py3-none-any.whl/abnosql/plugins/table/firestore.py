from base64 import b64decode
from base64 import b64encode
import functools
import json
import logging
import os
from os.path import expanduser
import sys
import typing as t

import pluggy  # type: ignore
import sqlglot
from sqlglot import exp

import abnosql.exceptions as ex
from abnosql.plugin import PM
from abnosql.table import check_exists_enabled
from abnosql.table import delete_item_post
from abnosql.table import delete_item_pre
from abnosql.table import get_item_post
from abnosql.table import get_item_pre
from abnosql.table import get_key_attrs
from abnosql.table import kms_process_query_items
from abnosql.table import parse_connstr
from abnosql.table import put_item_post
from abnosql.table import put_item_pre
from abnosql.table import TableBase
from abnosql.table import validate_query_attrs


hookimpl = pluggy.HookimplMarker('abnosql.table')

try:
    from google.api_core.exceptions import ClientError  # type: ignore
    from google.auth.exceptions import GoogleAuthError  # type: ignore
    from google.cloud import firestore  # type: ignore
except ImportError:
    MISSING_DEPS = True

OPERATORS = {
    exp.EQ: '==',
    exp.NEQ: '!=',
    exp.GT: '>',
    exp.GTE: '>=',
    exp.LT: '<',
    exp.LTE: '<=',
}


def firestore_ex_handler(raise_not_found: t.Optional[bool] = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientError as e:
                if raise_not_found and e.code in [404]:
                    raise ex.NotFoundException() from None
                raise ex.ValidationException(detail=e) from None
            except GoogleAuthError as e:
                raise ex.ConfigException(detail=e) from None
            except ex.NoSQLException:
                raise
            except Exception as e:
                raise ex.PluginException(detail=e) from None
        return wrapper
    return decorator


class Table(TableBase):

    @firestore_ex_handler()
    def __init__(
        self, pm: PM, name: str, config: t.Optional[dict] = None
    ) -> None:
        self.pm = pm
        self.name = name
        self.database = 'firestore'
        self.set_config(config)
        self.client = self.config.get('client', self.get_client())
        self.key_attrs = get_key_attrs(self.config)
        self.check_exists = check_exists_enabled(self.config)
        self.table = self.client.collection(name)
        self.docid_delim = self.config.get('docid_delim', ':')
        self.batch = None

    def get_client(self):
        kwargs = {}
        pc = parse_connstr()
        if kwargs is not None:
            kwargs.update({
                'project': pc.username,
                'database': pc.hostname
            })
            if pc.password not in ['', None]:
                kwargs['credentials'] = pc.password
        for attr in ['project', 'database', 'credentials']:
            for prefix in ['ABNOSQL_FIRESTORE_', 'GOOGLE_CLOUD_']:
                val = os.environ.get(prefix + attr.upper(), kwargs.get(attr))
                if val is not None:
                    kwargs[attr] = val
                break
        cred_file = os.path.join(*(
            (
                tuple(os.environ.get('APPDATA', ''))
                if sys.platform == 'win32'
                else (expanduser('~'), '.config')
            ) + (
                'gcloud',
                'application_default_credentials.json'
            )
        ))
        gac = 'GOOGLE_APPLICATION_CREDENTIALS'
        if gac not in os.environ and os.path.isfile(cred_file):
            os.environ[gac] = cred_file
        return firestore.Client(**kwargs)

    def _docid(self, **kwargs):
        item = dict(kwargs)
        key = [
            item.get(attr)
            for attr in self.key_attrs
            if item.get(attr)
        ]
        if len(key) > 2 or len(key) == 0:
            raise ValueError('key length must be 1 or 2')
        return self.docid_delim.join(key)

    @firestore_ex_handler()
    def set_config(self, config: t.Optional[dict]):
        if config is None:
            config = {}
        _config = self.pm.hook.set_config(table=self.name)
        if _config:
            config = t.cast(t.Dict, _config)
        self.config = config

    @firestore_ex_handler()
    def get_item(self, **kwargs) -> t.Optional[t.Dict]:
        audit_key, _ = get_item_pre(self, dict(**kwargs))

        doc = self.table.document(self._docid(**kwargs)).get()
        item = doc.to_dict() if doc.exists else None

        return get_item_post(self, dict(**kwargs), item, audit_key)

    @firestore_ex_handler()
    def put_item(
        self,
        item: t.Dict,
        update: t.Optional[bool] = False,
        audit_user: t.Optional[str] = None
    ) -> t.Dict:
        item, _ = put_item_pre(self, item, update, audit_user)

        # do update
        docid = self._docid(**item)
        ref = self.table.document(docid)
        if update is True:
            if self.batch:
                self.batch.update(ref, item)
            else:
                ref.update(item)

        # do create/replace
        else:
            if self.batch:
                self.batch.set(ref, item)
            else:
                ref.set(item)

        # firestore doesnt return updated item, so make this optional if needed
        # note encrypted attrs won't be decrypted
        if self.config.get('put_get') is True:
            item = self.table.document(docid).get().to_dict()

        return put_item_post(self, item, update, audit_user)

    @firestore_ex_handler()
    def put_items(
        self,
        items: t.Iterable[t.Dict],
        update: t.Optional[bool] = False,
        audit_user: t.Optional[str] = None
    ):
        if self.config.get('batchmode') is not False:
            self.batch = self.client.batch()
        for item in items:
            self.put_item(item, update=update, audit_user=audit_user)
        self.pm.hook.put_items_post(table=self.name, items=items)
        if self.config.get('batchmode') is not False:
            if self.batch is not None:
                self.batch.commit()
            self.batch = None

    @firestore_ex_handler()
    def delete_item(self, **kwargs):
        key = delete_item_pre(self, dict(kwargs))

        docid = self._docid(**kwargs)
        self.table.document(docid).delete()
        delete_item_post(self, key)

    @firestore_ex_handler()
    def query(
        self,
        key: t.Optional[t.Dict[str, t.Any]] = None,
        filters: t.Optional[t.Dict[str, t.Any]] = None,
        limit: t.Optional[int] = None,
        next: t.Optional[str] = None,
        index: t.Optional[str] = None
    ) -> t.Dict[str, t.Any]:
        filters = filters or {}
        key = key or {}
        validate_query_attrs(key, filters)
        parameters = {
            f'@{k}': v for k, v in
            (filters | key).items()
        }
        statement = 'SELECT * FROM table'
        op = 'WHERE'
        for param in parameters.keys():
            statement += f' {op} {param} = @{param}'
            op = 'AND'
        return self.query_sql(
            statement,
            parameters,
            limit=limit,
            next=next
        )

    @firestore_ex_handler()
    def query_sql(
        self,
        statement: str,
        parameters: t.Optional[t.Dict[str, t.Any]] = None,
        limit: t.Optional[int] = None,
        next: t.Optional[str] = None
    ) -> t.Dict[str, t.Any]:
        limit = limit or 100
        parameters = parameters or {}
        select = None
        try:
            select = sqlglot.parse_one(statement)
        except Exception:
            raise ex.ValidationException(detail='invalid SQL')
        if not isinstance(select, exp.Select):
            raise ex.ValidationException(detail='only SELECT is supported')

        # parse the sql using sqlglot (there must be a better way to do below)
        filters = []
        query = self.table
        where = select.find(exp.Where)
        if where:
            for cond in where.find_all(exp.Condition):
                if type(cond) not in OPERATORS.keys():
                    continue
                column = cond.this.name
                expr = cond.expression
                operator = OPERATORS.get(type(cond))  # type: ignore
                val = expr.this.name
                pval = parameters.get(f'@{val}')
                if isinstance(expr, exp.Column):
                    filters.append([column, operator, val])
                elif isinstance(expr, exp.Parameter) and pval is not None:
                    filters.append([column, operator, pval])

        logging.debug(f'query_sql() table: {self.name}, filters: {filters}')
        query = self.table

        for (col, op, val) in filters:
            query = query.where(col, op, val)

        # don't order as it messes up pagination
        if next is not None:
            query = query.start_at(
                json.loads(b64decode(next).decode())
            )

        if limit is not None:
            # needs to be + 1 so can see if any more left
            # as firestore doesnt tell us if anything left to paginate
            # so have to peak ahead with limit + 1
            query = query.limit(limit + 1)

        c = 0
        items = []
        last = None
        for doc in query.stream():
            c += 1
            item = doc.to_dict()
            if c < limit + 1:
                items.append(item)
            last = b64encode(json.dumps({
                k: item[k] for k in self.key_attrs
                if k in item
            }).encode()).decode()

        if c < limit + 1:
            last = None
        items = kms_process_query_items(self.config, items)
        return {
            'items': items,
            'next': last
        }
