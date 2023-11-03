{
    'name': "Travel Management",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail', 'sale', 'website'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
This module contains all information about travel management bookings, tour package, vehicles, invoices and more
     """,
    'data': [
        'security/travel_management_security_group.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',

        'data/sequence.xml',
        'data/schedule_action.xml',
        'data/service_type_data.xml',
        'data/booking_website_menu.xml',

        'wizard/pdf_report_wizard.xml',

        'views/travel_management_views.xml',
        'views/vehicle_views.xml',
        'views/tour_package_views.xml',
        'views/booking_view_form_template.xml',
        'views/snippet.xml',
        'views/boooking_template.xml',
        'views/travel_management_menu.xml',
        'views/tour_package_menu.xml',
        'views/vehicle_menu.xml',

        'report/report.xml',
        'report/pdf_template.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'travel_management/static/src/xml/booking_carousel.xml',
            'travel_management/static/src/js/snippet.js',
        ],
    },
}
