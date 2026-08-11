# -*- coding: utf-8 -*-
{
    'name': 'HSEQ Seguridad y Salud en el Trabajo',
    'summary': 'Módulo integrador SST: riesgos, incidentes, inspecciones, EPP y capacitaciones',
    'description': """
Módulo paraguas que agrupa la funcionalidad de Seguridad y Salud en el Trabajo:
riesgos SST, incidentes/accidentes, inspecciones, EPP y capacitaciones.
Al instalarlo se habilita toda la suite SST del sistema HSEQ.
""",
    'author': 'MAPEI Colombia',
    'website': 'https://www.mapei.com.co',
    'category': 'HSEQ',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'hseq_core',
        'hseq_risk',
        'hseq_incidents',
        'hseq_inspections',
        'hseq_epp',
        'hseq_training',
    ],
    'data': [],
    'installable': True,
}
