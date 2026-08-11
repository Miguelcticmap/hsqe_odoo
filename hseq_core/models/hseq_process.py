# -*- coding: utf-8 -*-
from odoo import fields, models


class HseqProcess(models.Model):
    _name = 'hseq.process'
    _description = 'Proceso HSEQ'
    _order = 'site_id, area_id, name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    area_id = fields.Many2one(
        'hseq.area', string='Área', required=True, ondelete='restrict', index=True)
    site_id = fields.Many2one(
        'hseq.site', related='area_id.site_id', string='Sede',
        store=True, index=True, readonly=True)
    responsible_id = fields.Many2one('res.users', string='Responsable')
    active = fields.Boolean(string='Activo', default=True)
    description = fields.Text(string='Descripción')
    activity_ids = fields.One2many('hseq.activity', 'process_id', string='Actividades')
