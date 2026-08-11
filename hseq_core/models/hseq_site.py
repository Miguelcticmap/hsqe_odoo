# -*- coding: utf-8 -*-
from odoo import fields, models


class HseqSite(models.Model):
    _name = 'hseq.site'
    _description = 'Sede HSEQ'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    code = fields.Char(string='Código', tracking=True)
    sequence = fields.Integer(string='Secuencia', default=10)
    address = fields.Char(string='Dirección')
    city = fields.Char(string='Ciudad')
    responsible_id = fields.Many2one(
        'res.users', string='Responsable', tracking=True)
    active = fields.Boolean(string='Activo', default=True)
    description = fields.Text(string='Descripción')
    area_ids = fields.One2many('hseq.area', 'site_id', string='Áreas')
    area_count = fields.Integer(compute='_compute_counts', string='Áreas #')
    process_count = fields.Integer(compute='_compute_counts', string='Procesos #')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código de la sede debe ser único.'),
    ]

    def _compute_counts(self):
        for site in self:
            site.area_count = len(site.area_ids)
            site.process_count = self.env['hseq.process'].search_count(
                [('site_id', '=', site.id)])
