{
    'name': 'Purchase Request',
    'version': '1.0',
    'summary': 'Employee Purchase Requests',
    'description': 'Allows employees to submit purchase requests to procurement',
    'depends': ['purchase', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_request_views.xml',
    ],
    'installable': True,
    'application': True,
}