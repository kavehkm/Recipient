# standard
from datetime import datetime
# internal
from .base_model import Column, Model


class Product(Model):
    """Product Model"""
    __table_name__ = 'Product'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    name = Column(str)
    price = Column(float)
    category_id = Column(int)


class ProductMap(Model):
    """Product Map Model"""
    __table_name__ = 'ProductMap'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    wpid = Column(int)
    last_update = Column(datetime)
    update_required = Column(bool)


class Category(Model):
    """Category Model"""
    __table_name__ = 'Category'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    name = Column(str)


class CategoryMap(ProductMap):
    """Category Map Model"""
    __table_name__ = 'CategoryMap'
    __primary_key__ = 'id'
