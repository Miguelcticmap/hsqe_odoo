# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqArea(models.Model):
    _name = 'hseq.area'
    _description = 'Área HSEQ'
    _order = 'site_id, name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    site_id = fields.Many2one(
        'hseq.site', string='Sede', required=True, ondelete='restrict', index=True)
    responsible_id = fields.Many2one('res.users', string='Responsable')
    active = fields.Boolean(string='Activo', default=True)
    description = fields.Text(string='Descripción')
    process_ids = fields.One2many('hseq.process', 'area_id', string='Procesos')

    @api.depends('name', 'site_id.name')
    def _compute_display_name(self):
        for area in self:
            if area.site_id:
                area.display_name = f"{area.site_id.name} / {area.name}"
            else:
                area.display_name = area.name
