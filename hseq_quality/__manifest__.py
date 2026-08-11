# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Calidad',
    'summary': 'Gestión de calidad y mejora continua',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_nonconformity', 'hseq_audit'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_quality_security.xml',
        'data/hseq_quality_data.xml',
        'views/hseq_quality_views.xml',
    ],
    'installable': True,
}
