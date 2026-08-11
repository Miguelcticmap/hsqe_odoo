# -*- coding: utf-8 -*-
{
    'name': 'HSEQ No Conformidades',
    'summary': 'Gestión de no conformidades y acciones correctivas',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_action_plan'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_nonconformity_security.xml',
        'data/hseq_nonconformity_data.xml',
        'views/hseq_nonconformity_views.xml',
    ],
    'installable': True,
}
