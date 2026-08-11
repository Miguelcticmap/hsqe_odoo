# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Auditorías',
    'summary': 'Planificación y ejecución de auditorías internas y externas',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_action_plan', 'hseq_nonconformity'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_audit_security.xml',
        'data/hseq_audit_data.xml',
        'views/hseq_audit_views.xml',
    ],
    'installable': True,
}
