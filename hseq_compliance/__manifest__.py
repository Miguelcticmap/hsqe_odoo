# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Compliance',
    'summary': 'Requisitos legales, obligaciones y estado de cumplimiento',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_action_plan'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_compliance_security.xml',
        'data/hseq_compliance_data.xml',
        'views/hseq_compliance_views.xml',
    ],
    'installable': True,
}
