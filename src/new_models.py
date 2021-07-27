# standard
from datetime import datetime
# internal
from src import table
from src import wc_api
from src import new_wc


class Model(object):
    """Recipient Model"""
    def __init__(self):
        self._connection = None

    def set_connection(self, connection):
        self._connection = connection


class Mappable(Model):
    """Recipient Mappable"""
    def mapped(self):
        pass

    def unmapped(self):
        pass

    def wc_mapped(self):
        pass

    def wc_unmapped(self):
        pass

    def wc_mapped_update(self, mapped):
        pass

    def add_map(self, moeinid, wcid, last_update):
        pass

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        pass

    def remove_map(self, moeinid):
        pass

    def export2wc(self, moein_object):
        pass

    def import2moein(self, wc_object):
        pass


class Product(Mappable):
    """Recipeint Product Model"""
    def __init__(self):
        super().__init__()
        # product table
        self.p = table.get('Product', 'id')
        # product map table
        self.pm = table.get('ProductMap', 'id')
        # category map table
        self.cm = table.get('CategoryMap', 'id')
        # wc product
        api = wc_api.get()
        self.wcp = new_wc.get(api, 'products')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.p.set_connection(connection)
        self.pm.set_connection(connection)
        self.cm.set_connection(connection)

    def mapped(self):
        mapped = []
        rows = self.p.inner_join(
            self.pm,
            'id',
            'id',
            [],
            ['wcid', 'last_update', 'update_required']
        )
        for row in rows:
            mapped.append({
                'id': row.id,
                'name': row.name,
                'price': row.price,
                'category_id': row.category_id,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        return mapped

    def unmapped(self):
        unmapped = []
        rows = self.p.left_outer_join(
            self.pm,
            'id',
            'id',
            []
        )
        for row in rows:
            unmapped.append({
                'id': row.id,
                'name': row.name,
                'price': row.price,
                'category_id': row.category_id,
            })
        return unmapped

    def wc_mapped(self):
        return [
            {'id': row.wcid}
            for row in self.pm.all('wcid')
        ]

    def wc_unmapped(self):
        ids = [row.wcid for row in self.pm.all('wcid')]
        return self.wcp.all(excludes=ids)

    def wc_mapped_update(self, mapped):
        self.wcp.update(mapped['wcid'], {
            'name': mapped['name'],
            'regular_price': str(mapped['price'])
        })
        self.pm.update({'last_update': datetime.now()}, id=mapped['id'])

    def add_map(self, moeinid, wcid, last_update):
        # check moeinid
        product = self.p.get('id', 'name', id=moeinid)
        # check wcid
        self.wcp.get(wcid)
        # every thing is ok lets create map
        fields = {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        }
        self.pm.create(fields)
        # extends fields
        fields['name'] = product.name
        return fields

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check moeinid
        product = self.p.get('id', 'name', id=new_moeinid)
        # check wcid
        self.wcp.get(new_wcid)
        fields = {
            'id': new_moeinid,
            'wcid': new_wcid
        }
        self.pm.update(fields, id=moeinid)
        # extends fields
        fields['name'] = product.name
        return fields

    def remove_map(self, moeinid):
        # check moeinid
        self.pm.get(id=moeinid)
        # remove map
        self.pm.delete(id=moeinid)

    def export2wc(self, product):
        # find wc_category
        wc_category = self.cm.get('wcid', id=product['category_id'])
        wc_product = self.wcp.create({
            'name': product['name'],
            'regular_price': str(product['price']),
            'categories': [{'id': wc_category.wcid}]
        })
        self.pm.create({
            'id': product['id'],
            'wcid': wc_product['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_product):
        # get first category
        wc_category = wc_product['categories'][0]
        category = self.cm.get('id', wcid=wc_category['id'])
        self.p.create({
            'name': wc_product['name'],
            'price': wc_product['regular_price'],
            'category_id': category.id
        })
        self.pm.create({
            'id': self.p.max_pk(),
            'wcid': wc_product['id'],
            'last_update': datetime.now()
        })


class Category(Mappable):
    """Recipient Category Model"""
    def __init__(self):
        super().__init__()
        # category table
        self.c = table.get('Category', 'id')
        # category map table
        self.cm = table.get('CategoryMap', 'id')
        # wc category
        api = wc_api.get()
        self.wcc = new_wc.get(api, 'products/categories')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.c.set_connection(connection)
        self.cm.set_connection(connection)

    def mapped(self):
        mapped = []
        rows = self.c.inner_join(
            self.cm,
            'id',
            'id',
            [],
            ['wcid', 'last_update', 'update_required']
        )
        for row in rows:
            mapped.append({
                'id': row.id,
                'name': row.name,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        return mapped

    def unmapped(self):
        unmapped = []
        rows = self.c.left_outer_join(
            self.cm,
            'id',
            'id',
            []
        )
        for row in rows:
            unmapped.append({
                'id': row.id,
                'name': row.name
            })
        return unmapped

    def wc_mapped(self):
        return [
            {'id': row.wcid}
            for row in self.cm.all('wcid')
        ]

    def wc_unmapped(self):
        ids = [row.wcid for row in self.cm.all('wcid')]
        return self.wcc.all(excludes=ids)

    def wc_mapped_update(self, mapped):
        self.wcc.update(mapped['wcid'], {
            'name': mapped['name']
        })
        self.cm.update({'last_update': datetime.now()}, id=mapped['id'])

    def add_map(self, moeinid, wcid, last_update):
        # check moeinid
        category = self.c.get('id', 'name', id=moeinid)
        # check wcid
        self.wcc.get(wcid)
        fields = {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        }
        self.cm.create(fields)
        fields['name'] = category.name
        return fields

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check moeinid
        category = self.c.get('id', 'name', id=new_moeinid)
        # check wcid
        self.wcc.get(new_wcid)
        fields = {
            'id': new_moeinid,
            'wcid': new_wcid
        }
        self.cm.update(fields, id=moeinid)
        fields['name'] = category.name
        return fields

    def remove_map(self, moeinid):
        self.cm.get(id=moeinid)
        self.cm.delete(id=moeinid)

    def export2wc(self, category):
        wc_category = self.wcc.create({
            'parent': 0,
            'name': category['name']
        })
        self.cm.create({
            'id': category['id'],
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_category):
        self.c.create({
            'name': wc_category['name']
        })
        self.cm.create({
            'id': self.c.max_pk(),
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })


class Invoice(Model):
    """Recipient Invoice Model"""
    def __init__(self):
        super().__init__()
        # invoice table
        self.i = table.get('Invoice', 'id')
        # invlice map table
        self.im = table.get('InvoiceMap', 'id')
        # item-line table
        self.il = table.get('ItemLine', 'invoice_id')
        # customer table
        self.cs = table.get('Customer', 'id')
        # customer map table
        self.csm = table.get('CustomerMap', 'id')
        # wc order
        api = wc_api.get()
        self.wco = new_wc.get(api, 'orders')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.i.set_connection(connection)
        self.im.set_connection(connection)
        self.il.set_connection(connection)
        self.cs.set_connection(connection)
        self.csm.set_connection(connection)
