class DoesNotExistsError(Exception):
    """Does Not Exists Error"""
    def __init__(self, table, *args):
        super().__init__(*args)
        self.table = table.capitalize()

    def __str__(self):
        return '{} does not exists.'.format(self.table)


class Table(object):
    """Database Table"""
    def __init__(self, table, pk, alias1, alias2):
        self.table = table
        self.pk = pk
        self.alias1 = alias1
        self.alias2 = alias2
        # connection
        self._connection = None

    def set_connection(self, connection):
        self._connection = connection

    @staticmethod
    def select(alias1=None, columns1=(), alias2=None, columns2=()):
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
    def where(conditions):
        parameters = []
        sql = ' WHERE '
        for column, value in conditions.items():
            sql += '{} = ? AND '.format(column)
            parameters.append(value)
        return sql.rstrip(' AND '), parameters

    def execute(self, sql, parameters=(), method=None):
        results = None
        cursor = self._connection.cursor()
        cursor.execute(sql, parameters)
        if method:
            results = getattr(cursor, method)()
        cursor.close()
        return results

    def max_pk(self):
        sql = 'SELECT MAX({}) FROM {}'.format(self.pk, self.table)
        return self.execute(sql, method='fetchval')

    def all(self, *columns):
        sql = self.select(columns1=columns)
        sql += ' FROM {}'.format(self.table)
        return self.execute(sql, method='fetchall')

    def filter(self, *columns, **conditions):
        parameters = []
        sql = self.select(columns1=columns)
        sql += ' FROM {}'.format(self.table)
        if conditions:
            _sql, parameters = self.where(conditions)
            sql += _sql
        return self.execute(sql, parameters, method='fetchall')

    def get(self, *columns, **conditions):
        parameters = []
        sql = self.select(columns1=columns)
        sql += ' FROM {}'.format(self.table)
        if conditions:
            _sql, parameters = self.where(conditions)
            sql += _sql
        obj = self.execute(sql, parameters, 'fetchone')
        if obj is None:
            raise DoesNotExistsError(self.table)
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
        return self.execute(sql, parameters)

    def update(self, fields, **conditions):
        parameters = []
        sql = 'UPDATE {} SET '.format(self.table)
        for column, value in fields.items():
            sql += '{} = ?, '.format(column)
            parameters.append(value)
        sql = sql.rstrip(', ')
        if conditions:
            _sql, _parameters = self.where(conditions)
            sql += _sql
            parameters.extend(_parameters)
        return self.execute(sql, parameters)

    def delete(self, **conditions):
        parameters = []
        sql = 'DELETE FROM {}'.format(self.table)
        if conditions:
            _sql, _parameters = self.where(conditions)
            sql += _sql
            parameters = _parameters
        return self.execute(sql, parameters)

    def inner_join(self, model, on1, on2, columns1, columns2):
        sql = self.select(self.alias1, columns1, self.alias2, columns2)
        sql += ' FROM {} AS {} INNER JOIN {} AS {}'.format(self.table, self.alias1, model.table, self.alias2)
        sql += ' ON {}.{} = {}.{}'.format(self.alias1, on1, self.alias2, on2)
        return self.execute(sql, method='fetchall')

    def left_outer_join(self, model, on1, on2, columns):
        sql = self.select(self.alias1, columns)
        sql += ' FROM {} AS {} LEFT JOIN {} AS {}'.format(self.table, self.alias1, model.table, self.alias2)
        sql += ' ON {}.{} = {}.{} WHERE {}.{} IS NULL'.format(self.alias1, on1, self.alias2, on2, self.alias2, on2)
        return self.execute(sql, method='fetchall')

    def right_outer_join(self, model, on1, on2, columns):
        sql = self.select(self.alias2, columns)
        sql += ' FROM {} AS {} RIGHT JOIN {} AS {}'.format(self.table, self.alias1, model.table, self.alias2)
        sql += ' ON {}.{} = {}.{} WHERE {}.{} IS NULL'.format(self.alias1, on1, self.alias2, on2, self.alias1, on1)
        return self.execute(sql, method='fetchall')


def get(table_name, primary_key, alias1='A', alias2='B'):
    return Table(table_name, primary_key, alias1, alias2)
