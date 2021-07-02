from src.wc.base_model import WCBaseModel


class Category(WCBaseModel):
    """WooCommerce Category Model"""
    ENDPOINT = 'products/categories'

    def create(self, name, slug, parent=0):
        data = {
            'name': name,
            'slug': slug,
            'parent': parent
        }
        return super().create(data)


class Product(WCBaseModel):
    """WooCommerce Product Model"""
    ENDPOINT = 'products'

    def create(self, name, slug, regular_price, parent_id=0):
        data = {
            'name': name,
            'slug': slug,
            'parent_id': parent_id,
            'regular_price': regular_price
        }
        return super().create(data)
