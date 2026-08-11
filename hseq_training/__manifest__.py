# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Capacitaciones',
    'summary': 'Plan anual de capacitación, sesiones, asistencia y certificados',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_training_security.xml',
        'data/hseq_training_data.xml',
        'views/hseq_training_views.xml',
    ],
    'installable': True,
}
