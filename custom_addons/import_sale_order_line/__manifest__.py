{
    'name': "Import Sale Order Lines",
    'version': '16.0.1.0.0',
    'depends': ['base', 'sale_management', 'account'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
This module shows a button in sale order by which we can import xls and we can get all the products and details in sale order line
""",
    'data': [
        'security/ir.model.access.csv',
        'wizard/xls_import_wizard.xml',
        'views/import_lines.xml',
    ],
    'installable': True,
    'application': True,

}
