# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Gestión de Riesgos',
    'summary': 'Identificación de peligros, evaluación y control de riesgos',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_action_plan'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_risk_security.xml',
        'data/hseq_risk_data.xml',
        'views/hseq_risk_views.xml',
    ],
    'installable': True,
}
