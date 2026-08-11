# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqActivity(models.Model):
    _name = 'hseq.activity'
    _description = 'Actividad HSEQ'
    _order = 'process_id, name'

    name = fields.Char(string='Nombre', required=True)
    process_id = fields.Many2one(
        'hseq.process', string='Proceso', required=True,
        ondelete='restrict', index=True)
    site_id = fields.Many2one(
        related='process_id.site_id', string='Sede', store=True, index=True)
    area_id = fields.Many2one(
        related='process_id.area_id', string='Área', store=True, index=True)
    routine = fields.Selection([
        ('routine', 'Rutinaria'),
        ('non_routine', 'No rutinaria'),
        ('emergency', 'Emergencia'),
    ], string='Tipo', default='routine')
    active = fields.Boolean(string='Activo', default=True)
    description = fields.Text(string='Descripción')
