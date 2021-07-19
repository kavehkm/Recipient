# internal
from .errors import DoesNotExistsError


class Column(object):
    """Model Column"""
    def __init__(self, t, wp=None):
        self.type = t
        self.wp = wp


class ModelBase(type):
    """Model Base MetaClass"""
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls._columns = {}
        for name, attr in attrs.items():
            if isinstance(attr, Column):
                new_cls._columns[name] = attr
        return new_cls


class Model(metaclass=ModelBase):
    """Model"""
    __table_name__ = None
    __primary_key__ = None
    # aliases
    ALIAS1 = 'A'
    ALIAS2 = 'B'

    def __init__(self):
        self.table = self.__table_name__
        self.pk = self.__primary_key__
        self._conn = None

    @property
    def connection(self):
        return self._conn

    @connection.setter
    def connection(self, conn):
        self._conn = conn

    @staticmethod
    def _select(alias1=None, columns1=(), alias2=None, columns2=()):
        sql = 'SELECT '
        c = alias1 + '.{}, ' if alias1 else '{}, '
        if columns1:
            for column in columns1:
                sql += c.format(column)
        else:
            sql += c.format('*')
        if alias2:
            if columns2:
                for column in columns2:
                    sql += '{}.{}, '.format(alias2, column)
            else:
                sql += '{}.*'.format(alias2)
        return sql.rstrip(', ')

    @staticmethod
    def _where(conditions):
        parameters = []
        sql = ' WHERE '
        for column, value in conditions.items():
            sql += '{} = ? AND '.format(column)
            parameters.append(value)
        return sql.rstrip(' AND '), parameters

    def _execute(self, sql, parameters=(), method=None):
        results = None
        with self._conn.cursor() as cursor:
            cursor.execute(sql, parameters)
            if method:
                results = getattr(cursor, method)()
        return results

    def get_max_pk(self):
        sql = 'SELECT MAX({}) FROM {}'.format(self.pk, self.table)
        return self._execute(sql, method='fetchval')

    def all(self, *columns):
        sql = self._select(columns1=columns)
        sql += ' FROM {}'.format(self.table)
        return self._execute(sql, method='fetchall')

    def filter(self, *columns, **conditions):
        parameters = []
        sql = self._select(columns1=columns)
        sql += ' FROM {}'.format(self.table)
        if conditions:
            _sql, parameters = self._where(conditions)
            sql += _sql
        return self._execute(sql, parameters, method='fetchall')

    def get(self, *columns, **conditions):
        parameters = []
        sql = self._select(columns1=columns)
        sql += ' FROM {}'.format(self.table)
        if conditions:
            _sql, parameters = self._where(conditions)
            sql += _sql
        obj = self._execute(sql, parameters, 'fetchone')
        if obj is None:
            raise DoesNotExistsError
        return obj

    def create(self, fields):
        parameters = []
        sql = 'INSERT INTO {}('.format(self.table)
        for column, value in fields.items():
            sql += '{}, '.format(column)
            parameters.append(value)
        sql = sql.rstrip(', ')
        sql += ') VALUES ('
        sql += ', '.join(['?' for _ in parameters]) + ')'
        return self._execute(sql, parameters)

    def update(self, fields, **conditions):
        parameters = []
        sql = 'UPDATE {} SET '.format(self.table)
        for column, value in fields.items():
            sql += '{} = ?, '.format(column)
            parameters.append(value)
        sql = sql.rstrip(', ')
        if conditions:
            _sql, _parameters = self._where(conditions)
            sql += _sql
            parameters.extend(_parameters)
        return self._execute(sql, parameters)

    def delete(self, **conditions):
        parameters = []
        sql = 'DELETE FROM {}'.format(self.table)
        if conditions:
            _sql, _parameters = self._where(conditions)
            sql += _sql
            parameters = _parameters
        return self._execute(sql, parameters)

    def inner_join(self, model, on1, on2, columns1, columns2):
        sql = self._select(self.ALIAS1, columns1, self.ALIAS2, columns2)
        sql += ' FROM {} AS {} INNER JOIN {} AS {}'.format(self.table, self.ALIAS1, model.table, self.ALIAS2)
        sql += ' ON {}.{} = {}.{}'.format(self.ALIAS1, on1, self.ALIAS2, on2)
        return self._execute(sql, method='fetchall')

    def left_outer_join(self, model, on1, on2, columns):
        sql = self._select(self.ALIAS1, columns)
        sql += ' FROM {} AS {} LEFT JOIN {} AS {}'.format(self.table, self.ALIAS1, model.table, self.ALIAS2)
        sql += ' ON {}.{} = {}.{} WHERE {}.{} IS NULL'.format(self.ALIAS1, on1, self.ALIAS2, on2, self.ALIAS2, on2)
        return self._execute(sql, method='fetchall')

    def right_outer_join(self, model, on1, on2, columns):
        sql = self._select(self.ALIAS2, columns)
        sql += ' FROM {} AS {} RIGHT JOIN {} AS {}'.format(self.table, self.ALIAS1, model.table, self.ALIAS2)
        sql += ' ON {}.{} = {}.{} WHERE {}.{} IS NULL'.format(self.ALIAS1, on1, self.ALIAS2, on2, self.ALIAS1, on1)
        return self._execute(sql, method='fetchall')
