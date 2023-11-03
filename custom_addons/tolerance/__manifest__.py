{
    'name': "Tolerance",
    'version': '16.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
This module shows information about tolerance
""",
    'data': [
        'security/ir.model.access.csv',

        'wizard/tolerance_wizard.xml',

        'views/tolerance_view.xml',
        'views/tolerance_orderline_view.xml',
        'views/tolerance_delivery_view.xml',
    ],
    'installable': True,
    'application': True,

}
