{
    "name": "Estate",
    "version": "1.0",
    "author": "Alexey Bormotov",
    "application": True,
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
}
