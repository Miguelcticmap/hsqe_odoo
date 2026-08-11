# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Indicadores',
    'summary': 'Indicadores HSEQ configurables con mediciones por sede y periodo',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_indicator_security.xml',
        'views/hseq_indicator_views.xml',
    ],
    'installable': True,
}
