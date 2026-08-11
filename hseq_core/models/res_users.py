# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    hseq_site_ids = fields.Many2many(
        'hseq.site', 'hseq_site_users_rel', 'user_id', 'site_id',
        string='Sedes HSEQ autorizadas',
        help='Sedes sobre las cuales el usuario puede consultar y gestionar '
             'información HSEQ. Si se deja vacío, el usuario podrá acceder '
             'a todas las sedes.')
