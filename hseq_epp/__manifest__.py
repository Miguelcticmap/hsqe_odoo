# -*- coding: utf-8 -*-
{
    'name': 'HSEQ EPP',
    'summary': 'Catálogo y entregas de Elementos de Protección Personal',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_epp_security.xml',
        'data/hseq_epp_data.xml',
        'views/hseq_epp_views.xml',
    ],
    'installable': True,
}
