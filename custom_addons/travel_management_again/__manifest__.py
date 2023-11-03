{
    'name': "Travel Management Again",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail', 'sale'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
This module contains all the common features of Sales Management and eCommerce.
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/service_type_data.xml',
        'view/booking_view.xml',
        'view/travel_vehicle_view.xml',
        'view/booking_menu.xml',
        'view/travel_vehicle_menu.xml',
    ],
    'installable': True,
    'application': True,

}