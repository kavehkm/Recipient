# internal
from src import table
from src import wc_api
from src import new_wc


class Model(object):
    """Recipient Model"""
    def set_connection(self, connection):
        pass

    def mapped(self):
        pass

    def unmapped(self):
        pass

    def wc_mapped(self):
        pass

    def wc_unmapped(self):
        pass

    def wc_mapped_update(self, moeinid):
        pass

    def add_map(self, moeinid, wcid, last_update):
        pass

    def edit_map(self, moeinid, kwargs):
        pass

    def remove_map(self, moeinid):
        pass

    def export2wc(self, moein_obj):
        pass

    def import2moein(self, wc_obj):
        pass


class Product(Model):
    """Recipeint Product Model"""
    def __init__(self):
        # product table
        self.p = table.get('Product', 'id')
        # product map table
        self.pm = table.get('ProductMap', 'id')
        # wc product
        api = wc_api.get()
        self.wcp = new_wc.get(api, 'products')

    def set_connection(self, connection):
        self.p.set_connection(connection)
        self.pm.set_connection(connection)

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
        ids = [row.wcid for row in pm.all('wcid')]
        return self.wcp.all(excludes=ids)

    def add_map(self, moeinid, wcid, last_update):
        # check moienid
        product = self.p.get('id', 'name', id=moeinid)
        # check wcid
        self.wcp.get(wcid)
        # every thing is ok lets create map
        fields = {
            'id': product.id,
            'wcid': wcid,
            'last_update': last_update
        }
        self.pm.create(fields)
        # extends fields
        fields['name'] = product.name
        return fields

    def edit_map(self, moeinid, kwargs):
        pass

    def remove_map(self, moeinid):
        # check moeinid
        self.pm.get(id=moeinid)
        # remove map
        self.pm.delete(id=moeinid)
