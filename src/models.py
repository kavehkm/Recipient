# standard
import re
from datetime import datetime
# internal
from src import wc
from src import wc_api
from src import settings as s
from src.translation import _
from src.table import DoesNotExists, Table
# jalali datetime
from jdatetime import datetime as jdatetime


##############
# Base Model #
##############
class Model(object):
    """Recipient Model"""
    def __init__(self):
        self._connection = None

    def set_connection(self, connection):
        self._connection = connection


##################
# Mappable Model #
##################
class Mappable(Model):
    """Recipient Mappable"""
    def mapped(self, update_required=False):
        pass

    def unmapped(self):
        pass

    def wc_mapped(self):
        pass

    def wc_unmapped(self):
        pass

    def wc_mapped_update(self, mapped):
        pass

    def add_map(self, moeinid, wcid):
        pass

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        pass

    def remove_map(self, moeinid):
        pass

    def export2wc(self, moein_object):
        pass

    def import2moein(self, wc_object):
        pass


#################
# Product Model #
#################
class Product(Mappable):
    """Recipient Product Model"""
    def __init__(self):
        super().__init__()
        # tables
        self.product = Table('KalaList', _('Product'))
        self.product_map = Table('ProductMap', _('ProductMap'))
        self.category_map = Table('CategoryMap', _('CategoryMap'))
        self.price_level = Table('PriceLevel', _('PriceLevel'))
        self.product_price = Table('KalaPrice', _('ProductPrice'))
        self.product_repository = Table('MojodiList', _('ProductRepository'))
        # woocommerce api
        self.woocommerce = wc.get(wc_api.get(), 'products')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.product.connection = connection
        self.product_map.connection = connection
        self.category_map.connection = connection
        self.price_level.connection = connection
        self.product_price.connection = connection
        self.product_repository.connection = connection

    @staticmethod
    def _int(value, default=0):
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default

    @staticmethod
    def getinfo(info):
        info = info or ''
        d = dict()
        for item in re.findall(r'\[[\w\d]+ .+\]', info):
            item = item.strip('[ ]').split(' ')
            key = item[0]
            try:
                value = item[1]
            except IndexError:
                value = ''
            d[key] = value
        return d

    @staticmethod
    def setinfo(info, d):
        for key, value in d.items():
            pattern = r'\[{} .+\]'.format(key)
            new = '[{} {}]'.format(key, value)
            info, replaced = re.subn(pattern, new, info)
            if not replaced:
                info = '\n'.join([info, new])
        return info.strip()

    def mapped(self, update_required=False):
        mapped = list()
        settings = s.get('invoices')
        params = [settings['repository'], s.INVOICES_SELL_PRICE_TYPE, settings['price_level']]
        sql = """
            SELECT
                P.ID, P.Name, P.GroupID, P.Info, PM.wcid, PM.last_update, PM.update_required, KP.FinalPrice, MA.Mojoodi
            FROM
                KalaList AS P
            INNER JOIN
                ProductMap AS PM ON P.ID = PM.id
            INNER JOIN
                KalaPrice AS KP ON P.ID = KP.KalaID
            LEFT JOIN
                dbo.Mojoodi_all('1000/00/00', '3000/00/00', ?, '23:59:59', 0) AS MA ON P.ID = MA.ID_Kala
            WHERE
                KP.Type = ? AND KP.PriceID = ?
        """
        # check for update required
        if update_required:
            sql += " AND PM.update_required = 1"
        for row in self.product.custom_sql(sql, params, method='fetchall'):
            mapped.append({
                'id': row.ID,
                'name': row.Name,
                'quantity': self._int(row.Mojoodi),
                'price': self._int(row.FinalPrice),
                'category_id': row.GroupID,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        return mapped

    def unmapped(self):
        unmapped = list()
        settings = s.get('invoices')
        params = [settings['repository'], s.INVOICES_SELL_PRICE_TYPE, settings['price_level']]
        sql = """
            SELECT
                P.ID, P.Name, P.GroupID, P.Info, KP.FinalPrice, MA.Mojoodi
            FROM
                KalaList AS P
            INNER JOIN
                CategoryMap AS CM ON P.GroupID = CM.id
            LEFT JOIN
                ProductMap AS PM ON P.ID = PM.id
            INNER JOIN
                KalaPrice AS KP ON P.ID = KP.KalaID
            LEFT JOIN
                dbo.Mojoodi_all('1000/00/00', '3000/00/00', ?, '23:59:59', 0) AS MA ON P.ID = MA.ID_Kala
            WHERE
                PM.id IS NULL AND KP.Type = ? AND KP.PriceID = ?
        """
        for row in self.product.custom_sql(sql, params, method='fetchall'):
            unmapped.append({
                'id': row.ID,
                'name': row.Name,
                'price': self._int(row.FinalPrice),
                'quantity': self._int(row.Mojoodi),
                'category_id': row.GroupID,
            })
        return unmapped

    def wc_mapped(self):
        return [
            {'wcid': product_map.wcid}
            for product_map in self.product_map.all('wcid')
        ]

    def wc_unmapped(self):
        exclude = ','.join([str(pm.wcid) for pm in self.product_map.all('wcid')])
        category = ','.join([str(cm.wcid) for cm in self.category_map.all('wcid')])
        return self.woocommerce.all(exclude=exclude, category=category, status='publish')

    def add_map(self, moeinid, wcid):
        # check product
        product = self.product.get('Name', ID=moeinid)
        # check woocommerce product
        self.woocommerce.get(wcid)
        # everything is ok, lets create map
        last_update = datetime.now()
        self.product_map.create({
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        })
        return {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update,
            'name': product.Name}

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check product
        new_product = self.product.get('Name', ID=new_moeinid)
        # check woocommerce product
        self.woocommerce.get(new_wcid)
        # everything is ok, lets update current map
        self.product_map.update({'id': new_moeinid, 'wcid': new_wcid}, id=moeinid)
        return {
            'id': new_moeinid,
            'wcid': new_wcid,
            'name': new_product.Name
        }

    def remove_map(self, moeinid):
        # check for map
        self.product_map.get(id=moeinid)
        # map exists, lets delete it
        self.product_map.delete(id=moeinid)

    def wc_mapped_update(self, mapped):
        category_map = self.category_map.get(id=mapped['category_id'])
        data = {
            'name': mapped['name'],
            'categories': [{'id': category_map.wcid}],
            'regular_price': str(mapped['price']),
            'stock_quantity': mapped['quantity']
        }
        # update woocommerce product
        self.woocommerce.update(mapped['wcid'], data)
        # update product map
        self.product_map.update({'last_update': datetime.now(), 'update_required': False}, id=mapped['id'])

    def export2wc(self, product):
        category_map = self.category_map.get(id=product['category_id'])
        data = {
            'name': product['name'],
            'categories': [{'id': category_map.wcid}],
            'regular_price': str(product['price']),
            'stock_quantity': product['quantity'],
            'manage_stock': True,
            'status': 'publish' if product['quantity'] else 'draft'
        }
        # create woocommerce product
        wc_product = self.woocommerce.create(data)
        # create product map
        self.product_map.create({
            'id': product['id'],
            'wcid': wc_product['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_product):
        product_id = None
        # check for sku hint
        if s.get('import_export')['sku_hint'] and wc_product['sku']:
            try:
                product = self.product.get('ID', Code=self._int(wc_product['sku']))
            except DoesNotExists:
                pass
            else:
                product_id = product.ID
        # if cannot find product by sku hinting, create new one
        if product_id is None:
            # check for category_map
            category_map = None
            for category in wc_product['categories']:
                try:
                    category_map = self.category_map.get(wcid=category['id'])
                    break
                except DoesNotExists:
                    continue
            # if cannot find category_map, raise Exception
            if category_map is None:
                raise Exception(_('CategoryMap for product {} does not exists.').format(wc_product['name']))
            # clean quantity and regualr_price value
            quantity = self._int(wc_product['stock_quantity'])
            regular_price = self._int(wc_product['regular_price'])
            # - create product
            self.product.create({
                'Name': wc_product['name'],
                'GroupID': category_map.id,
                'SellPrice': regular_price,
                'Code': self.product.max('Code') + 1,
                'MenuOrder': self.product.max('MenuOrder') + 1,
                'Unit2': 'عدد',
                'BuyPrice': 0,
                'SefareshPoint': 0,
                'ShortCut': 0,
                'Active': 1,
                'Maliat': 1,
                'UnitType': 0,
                'Info': '',
                'Weight': 0,
                'IncPerc': 0,
                'IncPrice': 0,
                'ValueCalcType': 0
            })
            product_id = self.product.max('ID')
            # - set price levels
            for pl in self.price_level.all():
                self.product_price.create({
                    'PriceID': pl.ID,
                    'KalaID': product_id,
                    'Type': s.INVOICES_BUY_PRICE_TYPE,
                    'Price': 0,
                    '[Percent]': 0,
                    'FinalPrice': 0,
                    'Takhfif': 0
                })
                self.product_price.create({
                    'PriceID': pl.ID,
                    'KalaID': product_id,
                    'Type': s.INVOICES_SELL_PRICE_TYPE,
                    'Price': regular_price,
                    '[Percent]': 0,
                    'FinalPrice': regular_price,
                    'Takhfif': 0
                })
            # - quantity
            if quantity:
                self.product_repository.create({
                    'IdKala': product_id,
                    'Tedad': quantity,
                    'SumPrice': regular_price * quantity,
                    'Price': regular_price,
                    'Anbar': s.get('invoices')['repository'],
                    'Tedad1': 0,
                    'Tedad2': 0
                })
        # create product map
        self.product_map.create({
            'id': product_id,
            'wcid': wc_product['id'],
            'last_update': datetime.now()
        })


##################
# Category Model #
##################
class Category(Mappable):
    """Recipient Category Model"""
    def __init__(self):
        super().__init__()
        # tables
        self.category = Table('GroupKala', _('Category'))
        self.category_map = Table('CategoryMap', _('CategoryMap'))
        # woocommerce api
        self.woocommerce = wc.get(wc_api.get(), 'products/categories')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.category.connection = connection
        self.category_map.connection = connection

    def hierarchy_name(self, category):
        # check for parent
        if not category['parent']:
            return category['name']
        try:
            parent = self.category.get(ID=category['parent'])
        except DoesNotExists:
            return category['name']
        else:
            parent = {
                'id': parent.ID,
                'name': parent.GroupKala,
                'parent': parent.ParentID
            }
            return self.hierarchy_name(parent) + '___' + category['name']

    def wc_hierarchy_name(self, category, categories):
        # detect name
        name = category.get('_name') or category['name']
        # check for parent
        if not category['parent']:
            return name
        parent = None
        for cat in categories:
            if cat['id'] == category['parent']:
                parent = cat
                break
        return self.wc_hierarchy_name(parent, categories) + '___' + name if parent else name

    def hierarchify(self, categories, woocommerce=False):
        for category in categories:
            category['_name'] = category['name']
            if woocommerce:
                category['name'] = self.wc_hierarchy_name(category, categories)
            else:
                category['name'] = self.hierarchy_name(category)
        categories.sort(key=lambda c: c['parent'])

    def mapped(self, update_required=False):
        mapped = list()
        sql = """
            SELECT
                C.ID, C.ParentID, C.GroupKala, CM.id, CM.wcid, CM.last_update, CM.update_required
            FROM
                GroupKala as C
            INNER JOIN
                CategoryMap AS CM ON C.ID = CM.id
        """
        # check for update required
        if update_required:
            sql += " WHERE CM.update_required = 1"
        for row in self.category.custom_sql(sql, method='fetchall'):
            mapped.append({
                'id': row.ID,
                'name': row.GroupKala,
                'parent': row.ParentID,
                'wcid': row.wcid,
                'last_update': row.last_update,
                'update_required': row.update_required
            })
        self.hierarchify(mapped)
        return mapped

    def unmapped(self):
        unmapped = list()
        sql = """
            SELECT
                C.ID, C.ParentID, C.GroupKala
            FROM
                GroupKala as C
            LEFT JOIN
                CategoryMap as CM ON C.ID = CM.id
            WHERE
                CM.id IS NULL
        """
        for row in self.category.custom_sql(sql, method='fetchall'):
            unmapped.append({
                'id': row.ID,
                'name': row.GroupKala,
                'parent': row.ParentID
            })
        self.hierarchify(unmapped)
        return unmapped

    def wc_mapped(self):
        return [
            {'wcid': category_map.wcid}
            for category_map in self.category_map.all('wcid')
        ]

    def wc_unmapped(self):
        unmapped = list()
        ids = [category_map.wcid for category_map in self.category_map.all('wcid')]
        categories = self.woocommerce.all()
        self.hierarchify(categories, woocommerce=True)
        for category in categories:
            if category['id'] not in ids:
                unmapped.append(category)
        return unmapped

    def add_map(self, moeinid, wcid):
        # check category and parent
        category = self.category.get(ID=moeinid)
        if category.ParentID:
            self.category_map.get(id=category.ParentID)
        category = {
            'id': category.ID,
            'name': category.GroupKala,
            'parent': category.ParentID
        }
        # check woocommerce category
        self.woocommerce.get(wcid)
        # everything is ok, lets create map
        last_update = datetime.now()
        self.category_map.create({
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update
        })
        return {
            'id': moeinid,
            'wcid': wcid,
            'last_update': last_update,
            'name': self.hierarchy_name(category)
        }

    def edit_map(self, moeinid, new_moeinid, new_wcid):
        # check new category and parent
        new_category = self.category.get(ID=moeinid)
        if new_category.ParentID:
            self.category_map.get(id=new_category.ParentID)
        new_category = {
            'id': new_category.ID,
            'name': new_category.GroupKala,
            'parent': new_category.ParentID
        }
        # check for new woocommerce category
        self.woocommerce.get(new_wcid)
        # everything is ok, lets update current map
        self.category_map.update({'id': new_moeinid, 'wcid': new_wcid}, id=moeinid)
        return {
            'id': new_moeinid,
            'wcid': new_wcid,
            'name': self.hierarchy_name(new_category)
        }

    def remove_map(self, moeinid):
        # check for map
        self.category_map.get(id=moeinid)
        # map exists, lets delete it
        self.category_map.delete(id=moeinid)

    def wc_mapped_update(self, mapped):
        data = {
            'name': mapped['_name'],
            'parent': mapped['parent']
        }
        # check for parent
        if mapped['parent']:
            parent = self.category_map.get(id=mapped['parent'])
            data['parent'] = parent.wcid
        # update woocommerce category
        self.woocommerce.update(mapped['wcid'], data)
        # update category map
        self.category_map.update({'last_update': datetime.now(), 'update_required': False}, id=mapped['id'])

    def export2wc(self, category):
        data = {
            'name': category['_name'],
            'parent': category['parent']
        }
        # check for parent
        if category['parent']:
            parent = self.category_map.get(id=category['parent'])
            data['parent'] = parent.wcid
        # create woocommerce category
        wc_category = self.woocommerce.create(data)
        self.category_map.create({
            'id': category['id'],
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })

    def import2moein(self, wc_category):
        # check for category name
        if len(wc_category['_name']) > 50:
            raise Exception(_('Category {} name is too long.').format(wc_category['_name']))
        # check for parent
        if wc_category['parent']:
            parent = self.category_map.get(wcid=wc_category['parent'])
            parent_id = parent.id
        else:
            parent_id = 0
        # create category
        self.category.create({
            'GroupKala': wc_category['_name'],
            'ParentID': parent_id
        })
        # create map
        self.category_map.create({
            'id': self.category.max('ID'),
            'wcid': wc_category['id'],
            'last_update': datetime.now()
        })


#################
# Invoice Model #
#################
class Invoice(Model):
    """Recipient Invoice Model"""
    def __init__(self):
        super().__init__()
        # tables
        self.invoice = Table('Factor1', _('Invoice'))
        self.invoice_map = Table('InvoiceMap', _('InvoiceMap'))
        self.customer = Table('AshkhasList', _('Customer'))
        self.customer_map = Table('CustomerMap', _('CustomerMap'))
        self.product = Table('KalaList', _('Product'))
        self.product_map = Table('ProductMap', _('ProductMap'))
        self.line_item = Table('Faktor2', _('LineItem'))
        # woocommerce
        self.woocommerce = wc.get(wc_api.get(), 'orders')

    def set_connection(self, connection):
        super().set_connection(connection)
        self.invoice.connection = connection
        self.invoice_map.connection = connection
        self.customer.connection = connection
        self.customer_map.connection = connection
        self.product.connection = connection
        self.product_map.connection = connection
        self.line_item.connection = connection

    def items(self, line_items):
        items = list()
        for item in line_items:
            # get map
            product_map = self.product_map.get(wcid=item['product_id'])
            # get mapped product
            product = self.product.get('ID', 'Name', ID=product_map.id)
            # calculate required details
            price = int(item['price'])              # price = regular_price - discount
            quantity = item['quantity']             # quantity
            subtotal = int(item['subtotal'])        # subtotal = regular_price * quantity
            total = int(item['total'])              # total = price * quantity
            regular_price = subtotal // quantity    # regular_price = subtotal // quantity
            discount = subtotal - total             # discount = subtotal = total
            items.append({
                'id': product.ID,
                'name': product.Name,
                'quantity': quantity,
                'price': price,
                'regular_price': regular_price,
                'subtotal': subtotal,
                'total': total,
                'discount': discount
            })
        return items

    @staticmethod
    def items_subtotal(line_items):
        subtotal = 0
        for item in line_items:
            subtotal += int(item['subtotal'])
        return subtotal

    @staticmethod
    def items_total(line_items):
        total = 0
        for item in line_items:
            total += int(item['total'])
        return total

    @staticmethod
    def items_discount(line_items):
        discount = 0
        for item in line_items:
            discount += int(item['subtotal']) - int(item['total'])
        return discount

    def orders(self):
        settings = s.get('orders')
        orders = self.woocommerce.all(
            exclude=','.join([str(im.wcid) for im in self.invoice_map.all()]),
            status=','.join(settings['status']),
            after=settings['after'],
            before=settings['before']
        )
        for order in orders:
            order['created_date'] = datetime.fromisoformat(order['date_created_gmt'])
            order['items'] = self.items(order['line_items'])
            order['items_subtotal'] = self.items_subtotal(order['line_items'])
            order['items_total'] = self.items_total(order['line_items'])
            order['items_discount'] = self.items_discount(order['line_items'])
            order['discount'] = int(order['discount_total']) - self.items_discount(order['line_items'])
            order['first_name'] = order['billing']['first_name'] or order['shipping']['first_name']
            order['last_name'] = order['billing']['last_name'] or order['shipping']['last_name']
        return orders

    def update_order(self, order_id, data):
        self.woocommerce.update(order_id, data)

    def saved(self):
        saved = list()
        sql = """
            SELECT
                I.ID, I.FactorNo, I.Date, I.Time, IM.wcid, IM.last_update, C.Code, C.Name
            FROM
                Factor1 AS I
            INNER JOIN
                InvoiceMap AS IM ON IM.id = I.ID
            INNER JOIN
                AshkhasList as C ON C.ID = I.IDShakhs
            WHERE
                I.Tmp = 0 AND Converted = 0 AND Type = 0
        """
        for row in self.invoice.custom_sql(sql, method='fetchall'):
            saved.append({
                'id': row.ID,
                'No': row.FactorNo,
                'date': row.Date,
                'time': row.Time,
                'order_id': row.wcid,
                'saved_date': row.last_update,
                'customer_code': row.Code,
                'customer_name': row.Name
            })
        return saved

    def save(self, order):
        # get settings
        settings = s.get('invoices')
        # current date and time in jalali calendar
        date_frmt = '%Y/%m/%d'
        time_frmt = '%H:%M:%S'
        current_date = jdatetime.now().date().strftime(date_frmt)
        current_time = jdatetime.now().date().strftime(time_frmt)
        # order date and time in jalali calendar
        order_datetime = jdatetime.fromgregorian(datetime=order['created_date'])
        order_date = order_datetime.date().strftime(date_frmt)
        order_time = order_datetime.time().strftime(time_frmt)
        # detect customer
        if not order['customer_id']:
            customer_id = settings['guest']
        else:
            try:
                customer_map = self.customer_map.get(wcid=order['customer_id'])
                customer_id = customer_map.id
            except DoesNotExists:
                self.customer.create({
                    'Code': self.customer.max('Code') + 1,
                    'Fname': order['first_name'],
                    'LName': order['last_name'],
                    'Name': '{} {}'.format(order['first_name'], order['last_name']),
                    'BuyPriceLevel': settings['price_level'],
                    'SellPriceLevel': settings['price_level'],
                    'StartDate': current_date,
                    'Prefix': '',
                    'ShiftTo': '23:59:59',
                    'ShiftFrom': '00:00:00',
                    'Visitor': 0,
                    'CarryPrice': 0,
                    'VisitorBed': 0,
                    'EtebarNaghd': 0,
                    'VisitorPerc': 0,
                    'EtebarCheque': 0,
                    'MablaghAvalDore': 0,
                })
                customer_id = self.customer.max('ID')
                self.customer_map.create({
                    'id': customer_id,
                    'wcid': order['customer_id'],
                    'last_update': datetime.now()
                })
        # get next invoice No
        invoice_no = self.invoice.custom_sql("SELECT dbo.NewFactorNo(?)", [settings['type']], method='fetchval')
        # prepare invoice fields
        fields = {
            'FactorNo': invoice_no,
            'FishNo': invoice_no,
            'Type': settings['type'],
            'IDShakhs': customer_id,
            'UserID': 1,
            'Date': order_date,
            'Time': order_time,
            'PaymentDate': order_date,
            'DeliverDate': order_date,
            'InsertDate': current_date,
            'InsertTime': current_time,
            'Info': '',
            'JamKol': int(order['total']),
            'GmeFactor': order['items_subtotal'],
            'MandeFactor': int(order['total']),
            'Maliat': int(order['total_tax']),
            'Takhfif': order['discount'],
            'TakhfifItem': order['items_discount'],
            'CarryPrice': int(order['shipping_total']),
            'CarryType': 0,
            'Nagd': 0,
            'Nagd2': 0,
            'Naseh': 0,
            'Naseh2': 0,
            'Chek': 0,
            'Chek2': 0,
            'Anbar': 0,
            'Confirmed': 0,
            'VisitorPrice': 0,
            'VisitorPerc': 0,
            'PaymentValue': 0,
            'PaymentType': 0,
            'Tmp': 0,
            'Converted': 0,
            'MaliatPerc': 0,
            'ServicePerc': 0,
            'ServicePrice': 0
        }
        # check for info
        if fields['CarryPrice']:
            fields['Info'] = _('carry price: {}').format(fields['CarryPrice'])
        # create invoice
        self.invoice.create(fields)
        invoice_id = self.invoice.max('ID')
        # insert items
        for i, item in enumerate(order['items'], 1):
            self.line_item.create({
                'FactorID': invoice_id,
                'IDKala': item['id'],
                'Tedad': item['quantity'],
                'Tedad1': 0,
                'Tedad2': item['quantity'],
                'TedadStr': str(item['quantity']),
                'Price': item['regular_price'],
                'SumPrice': int(item['total']),
                'Takhfif': item['discount'],
                'TakhfifPerc': 0,
                'TakhfifPerItem': 0,
                'TakhfifIsGift': 0,
                'Anbar': settings['repository'],
                'Info': '',
                'Row': i,
                'VisitorPrice': 0,
                'VisitorPerc': 0,
                'PaymentValue': 0,
                'PaymentType': 0,
                'PaymentDate': order_date,
                'JozDarKol': 0,
                'Maliat': 0,
                'Height': 0,
                'Width': 0,
                'Thick': 0,
                'Density': 0,
                'UnitType': 0,
                'Amount': 0,
                'Overhead': 0,
                'Gift': 0,
                'Value': 0,
                'PriceLevelID': settings['price_level'],
                'ValueEdited': 0
            })
        # create map
        self.invoice_map.create({
            'id': invoice_id,
            'wcid': order['id'],
            'last_update': datetime.now()
        })

    def remove(self, order_id):
        # find invoice id
        invoice = self.invoice_map.get(wcid=order_id)
        # remove related items to invoice
        self.line_item.delete(FactorID=invoice.id)
        # remove invoice
        self.invoice.delete(ID=invoice.id)
        # remove map
        self.invoice_map.delete(id=invoice.id)
