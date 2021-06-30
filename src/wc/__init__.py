from src.wc.base_model import WCBaseModel


class Category(WCBaseModel):
    """WooCommerce Category Model"""
    ENDPOINT = 'products/categories'


class Product(WCBaseModel):
    """WooCommerce Product Model"""
    ENDPOINT = 'products'
