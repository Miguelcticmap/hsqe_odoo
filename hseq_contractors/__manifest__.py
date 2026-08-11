# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Contratistas',
    'summary': 'Habilitación y control documental de contratistas',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core'],
    'data': [
        'security/ir.model.access.csv',
        'data/hseq_contractor_data.xml',
        'views/hseq_contractor_views.xml',
    ],
    'installable': True,
}
