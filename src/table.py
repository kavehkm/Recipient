# internal
from src.translation import _


##############
# Exceptions #
##############
class DoesNotExists(Exception):
    """Does Not Exists Exception"""
    def __init__(self, name, conditions):
        self.name = name
        self.conditions = conditions

    def __str__(self):
        msg = '{} {} '.format(self.name, _('with'))
        for column, value in self.conditions.items():
            msg += '{}:{}, '.format(column, value)
        return msg.rstrip(', ') + _(' does not exists.')


##################
# Database Table #
##################
class Table(object):
    """Database Table"""
    def __init__(self, table, object_name=None):
        self.table = table
        self.object_name = object_name or table
        # connection
        self._connection = None

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, conn):
        self._connection = conn

    @staticmethod
    def select(*columns):
        return 'SELECT {}'.format(', '.join(columns) if columns else '*')

    @staticmethod
    def where(conditions):
        params = list()
        sql = ' WHERE '
        for column, value in conditions.items():
            sql += '{} = ? AND '.format(column)
            params.append(value)
        return sql.rstrip(' AND '), params

    def execute(self, sql, params=(), method=None):
        results = None
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        if method:
            results = getattr(cursor, method)()
        cursor.close()
        return results

    def max(self, column):
        sql = 'SELECT MAX({}) FROM {}'.format(column, self.table)
        return self.execute(sql, method='fetchval')

    def all(self, *columns):
        sql = self.select(*columns)
        sql += ' FROM {}'.format(self.table)
        return self.execute(sql, method='fetchall')

    def filter(self, *columns, **conditions):
        params = list()
        sql = self.select(*columns)
        sql += ' FROM {}'.format(self.table)
        if conditions:
            _sql, params = self.where(conditions)
            sql += _sql
        return self.execute(sql, params, method='fetchall')

    def get(self, *columns, **conditions):
        params = list()
        sql = self.select(*columns)
        sql += ' FROM {}'.format(self.table)
        if conditions:
            _sql, params = self.where(conditions)
            sql += _sql
        obj = self.execute(sql, params, method='fetchone')
        if obj is None:
            raise DoesNotExists(self.object_name, conditions)
        return obj

    def create(self, fields):
        params = list()
        sql = 'INSERT INTO {}('.format(self.table)
        for column, value in fields.items():
            sql += '{}, '.format(column)
            params.append(value)
        sql = sql.rstrip(', ')
        sql += ') VALUES ('
        sql += ', '.join(['?' for _ in params]) + ')'
        return self.execute(sql, params)

    def update(self, fields, **conditions):
        params = list()
        sql = 'UPDATE {} SET '.format(self.table)
        for column, value in fields.items():
            sql += '{} = ?, '.format(column)
            params.append(value)
        sql = sql.rstrip(', ')
        if conditions:
            _sql, _params = self.where(conditions)
            sql += _sql
            params.extend(_params)
        return self.execute(sql, params)

    def delete(self, **conditions):
        params = list()
        sql = 'DELETE FROM {}'.format(self.table)
        if conditions:
            _sql, _params = self.where(conditions)
            sql += _sql
            params = _params
        return self.execute(sql, params)

    def custom_sql(self, sql, params=(), method=None):
        return self.execute(sql, params, method)
