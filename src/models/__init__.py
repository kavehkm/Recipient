# standard
from datetime import datetime
# internal
from .base_model import Column, Model


class ProductMap(Model):
    """Product Map Model"""
    __table_name__ = 'ProductMap'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    wpid = Column(int)
    last_update = Column(datetime)
    update_required = Column(bool)


class CategoryMap(ProductMap):
    """Category Map Model"""
    __table_name__ = 'CategoryMap'
    __primary_key__ = 'id'


class CustomerMap(ProductMap):
    """Customer Map Model"""
    __table_name__ = 'CustomerMap'
    __primary_key__ = 'id'


class SavedOrder(Model):
    """Saved Order Model"""
    __table_name__ = 'SavedOrder'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    invoice_id = Column(int)


class Customer(Model):
    """Customer Model"""
    __table_name__ = 'Customer'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    firstname = Column(str)
    lastname = Column(str)


class Category(Model):
    """Category Model"""
    __table_name__ = 'Category'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    name = Column(str)


class Product(Model):
    """Product Model"""
    __table_name__ = 'Product'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    name = Column(str)
    price = Column(float)
    category_id = Column(int)


class Invoice(Model):
    """Invoice Model"""
    __table_name__ = 'Invoice'
    __primary_key__ = 'id'
    # columns
    id = Column(int)
    customer_id = Column(int)
    created_date = Column(datetime)


class ItemLine(Model):
    """Item Line Model"""
    __table_name__ = 'ItemLine'
    __primary_key__ = 'order_id'
    # columns
    order_id = Column(int)
    product_id = Column(int)
    quantity = Column(int)
