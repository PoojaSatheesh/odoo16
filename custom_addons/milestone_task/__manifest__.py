{
    'name': "Milestone task",
    'version': '16.0.1.0.0',
    'depends': ['base', 'sale_management', 'sale_project'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
This module creates a projects and its subtasks by checking the milestone given in sale order line
""",
    'data': [
        'views/milestone_view.xml',
    ],
    'installable': True,
    'application': True,

}
