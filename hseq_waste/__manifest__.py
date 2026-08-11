# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Gestión de Residuos',
    'summary': 'Registro y disposición de residuos por sede',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_waste_security.xml',
        'data/hseq_waste_data.xml',
        'views/hseq_waste_views.xml',
    ],
    'installable': True,
}
