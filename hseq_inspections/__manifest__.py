# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Inspecciones',
    'summary': 'Plantillas de inspección, ejecución de inspecciones y hallazgos',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_action_plan'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_inspection_security.xml',
        'data/hseq_inspection_data.xml',
        'views/hseq_inspection_views.xml',
    ],
    'installable': True,
}
