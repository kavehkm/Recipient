class Column(object):
    """Model Column"""
    def __init__(self, name, wp_name):
        self.name = name
        self.wp_name = wp_name


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

    def __init__(self):
        self.table = self.__table_name__
        self.pk = self.__primary_key__
        self._conn = None

    @property
    def columns(self):
        return self._columns

    @property
    def connection(self):
        return self._conn

    @connection.setter
    def connection(self, conn):
        self._conn = conn

    def _2columns(self, properties):
        columns = {}
        for prop, value in properties.items():
            c = self._columns.get(prop)
            if c:
                columns[c.name] = value
        return columns

    def _select(self):
        sql = 'SELECT '
        for name, column in self._columns.items():
            sql += '{} AS {}, '.format(column.name, name)
        return sql.rstrip(', ')

    def _where(self, conditions):
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

    def all(self):
        sql = self._select()
        sql += ' FROM {}'.format(self.table)
        return self._execute(sql, method='fetchall')

    def filter(self, **conditions):
        parameters = []
        sql = self._select()
        sql += ' FROM {}'.format(self.table)
        conditions = self._2columns(conditions)
        if conditions:
            s, p = self._where(conditions)
            sql += s
            parameters = p
        return self._execute(sql, parameters, method='fetchall')

    def get(self, pk):
        sql = self._select()
        sql += ' FROM {} WHERE {} = ?'.format(self.table, self.pk)
        return self._execute(sql, [pk], method='fetchone')

    def create(self, fields):
        parameters = []
        sql = 'INSERT INTO {}('.format(self.table)
        for column, value in self._2columns(fields).items():
            sql += '{}, '.format(column)
            parameters.append(value)
        sql = sql.rstrip(', ')
        sql += ') VALUES ('
        sql += ', '.join(['?' for _ in parameters]) + ')'
        return self._execute(sql, parameters)

    def update(self, fields, **conditions):
        parameters = []
        sql = 'UPDATE {} SET '.format(self.table)
        for column, value in self._2columns(fields).items():
            sql += '{} = ?, '.format(column)
            parameters.append(value)
        sql = sql.rstrip(', ')
        conditions = self._2columns(conditions)
        if conditions:
            s, p = self._where(conditions)
            sql += s
            parameters.extend(p)
        return self._execute(sql, parameters)

    def delete(self, **conditions):
        parameters = []
        sql = 'DELETE FROM {}'.format(self.table)
        conditions = self._2columns(conditions)
        if conditions:
            s, p = self._where(conditions)
            sql += s
            parameters = p
        return self._execute(sql, parameters)
