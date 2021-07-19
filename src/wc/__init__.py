from .base_model import WCBaseModel


class Category(WCBaseModel):
    """WooCommerce Category Model"""
    ENDPOINT = 'products/categories'

    def create(self, name, parent=0):
        data = {
            'name': name,
            'parent': parent
        }
        return super().create(data)


class Product(WCBaseModel):
    """WooCommerce Product Model"""
    ENDPOINT = 'products'

    def create(self, name, regular_price, categories, parent_id=0):
        cats = [{'id': category} for category in categories]
        data = {
            'name': name,
            'parent_id': parent_id,
            'categories': cats,
            'regular_price': regular_price
        }
        return super().create(data)


class Order(WCBaseModel):
    """WooCommerce Order Model"""
    ENDPOINT = 'orders'
