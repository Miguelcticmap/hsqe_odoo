# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Incidentes y Accidentes',
    'summary': 'Reporte, investigación y cierre de incidentes, accidentes y casi accidentes',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core', 'hseq_action_plan'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_incident_security.xml',
        'data/hseq_incident_data.xml',
        'views/hseq_incident_views.xml',
    ],
    'installable': True,
}
