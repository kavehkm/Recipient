# internal
from src.translation import _


MESSAGES = [
    #############################################
    # WooCommerce: product (0-18)->slice(0, 19) #
    #############################################
    _('WooCommerce Products'),                                         # 00
    _('Moein Products'),                                               # 01
    _('Product not found.'),                                           # 02
    _('Cannot load options.'),                                         # 03
    _('Cannot load registered Products.'),                             # 04
    _('Cannot load unregistered Products.'),                           # 05
    _('Edit Product'),                                                 # 06
    _('Add new Product'),                                              # 07
    _('Add all Products...'),                                          # 08
    _('Update all Products...'),                                       # 09
    _('Cannot add all Products.'),                                     # 10
    _('All Products added successfully.'),                             # 11
    _('Cannot update all Products.'),                                  # 12
    _('All Products updated successfully.'),                           # 13
    _('Cannot save Product.'),                                         # 14
    _('Product saved successfully.'),                                  # 15
    _('Are your sure?'),                                               # 16
    _('Cannot remove Product.'),                                       # 17
    _('Product removed successfully.'),                                # 18
    ################################################
    # WooCommerce: category (19-37)->slice(19, 38) #
    ################################################
    _('WooCommerce Categories'),
    _('Moein Categories'),
    _('Category not found.'),
    _('Cannot load options.'),
    _('Cannot load registered Categories.'),
    _('Cannot load unregistered Categories.'),
    _('Edit Category'),
    _('Add New Category'),
    _('Add all Categories...'),
    _('Update all Categories...'),
    _('Cannot add all Categories.'),
    _('All Categories added successfully.'),
    _('Cannot update all Categories.'),
    _('All Categories updated successfully.'),
    _('Cannot save Category.'),
    _('Category saved successfully.'),
    _('Are you sure?'),
    _('Cannot remove Category.'),
    _('Category removed successfully.')
]


def get(index):
    return MESSAGES[index]
