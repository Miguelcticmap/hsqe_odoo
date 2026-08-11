# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Gestión Documental',
    'summary': 'Control de documentos, versiones, aprobaciones y vigencias',
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['hseq_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/hseq_document_security.xml',
        'data/hseq_document_data.xml',
        'views/hseq_document_views.xml',
    ],
    'installable': True,
}
