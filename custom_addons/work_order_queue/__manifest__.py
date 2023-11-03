{
    'name': "Work Order Queue",
    'version': '16.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
This model shows information about machines materials recived and all inside sales module
""",
    'data': [
        'security/ir.model.access.csv',

        'views/machine_view.xml',
        'views/sale_order_line_view.xml',
        'views/work_order_view.xml',
    ],
    'installable': True,
    'application': True,

}
