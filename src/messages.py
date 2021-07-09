MESSAGES = [
    #############################################
    # WooCommerce: product (0-18)->slice(0, 19) #
    #############################################
    'WooCommerce Products',                                         # 00
    'Moein Products',                                               # 01
    'Product not found.',                                           # 02
    'Cannot load options.',                                         # 03
    'Cannot load registered Products.',                             # 04
    'Cannot load unregistered Products.',                           # 05
    'Edit Product',                                                 # 06
    'Add new Product',                                              # 07
    'Add all Products...',                                          # 08
    'Update all Products...',                                       # 09
    'Cannot add all Products.',                                     # 10
    'All Products added successfully.',                             # 11
    'Cannot update all Products.',                                  # 12
    'All Products updated successfully.',                           # 13
    'Cannot save Product.',                                         # 14
    'Product saved successfully.',                                  # 15
    'Are your sure?',                                               # 16
    'Cannot remove Product.',                                       # 17
    'Product removed successfully.',                                # 18
    ################################################
    # WooCommerce: category (19-37)->slice(19, 38) #
    ################################################
    'WooCommerce Categories',
    'Moein Categories',
    'Category not found.',
    'Cannot load options.',
    'Cannot load registered Categories.',
    'Cannot load unregistered Categories.',
    'Edit Category',
    'Add New Category',
    'Add all Categories...',
    'Update all Categories...',
    'Cannot add all Categories.',
    'All Categories added successfully.',
    'Cannot update all Categories.',
    'All Categories updated successfully.',
    'Cannot save Category.',
    'Category saved successfully.',
    'Are you sure?',
    'Cannot remove Category.',
    'Category removed successfully.'
]


def get(index):
    return MESSAGES[index]
