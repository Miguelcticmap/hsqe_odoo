# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Dashboard',
    'summary': 'Panel de control HSEQ MAPEI con indicadores por sede',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'hseq_core',
        'hseq_action_plan',
        'hseq_risk',
        'hseq_incidents',
        'hseq_inspections',
        'hseq_nonconformity',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hseq_dashboard_views.xml',
    ],
    'installable': True,
}
