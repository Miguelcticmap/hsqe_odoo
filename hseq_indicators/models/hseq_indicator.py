# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqIndicator(models.Model):
    _name = 'hseq.indicator'
    _description = 'Indicador HSEQ'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    code = fields.Char(string='Código')
    domain_type = fields.Selection([
        ('sst', 'SST'),
        ('quality', 'Calidad'),
        ('environment', 'Ambiental'),
        ('compliance', 'Compliance'),
        ('management', 'Gestión'),
    ], string='Dominio', default='sst', required=True, tracking=True)
    uom = fields.Char(string='Unidad de medida', default='%')
    frequency = fields.Selection([
        ('monthly', 'Mensual'),
        ('quarterly', 'Trimestral'),
        ('semiannual', 'Semestral'),
        ('annual', 'Anual'),
    ], string='Frecuencia de medición', default='monthly', required=True)
    target = fields.Float(string='Meta', tracking=True)
    target_direction = fields.Selection([
        ('up', 'Mayor es mejor'),
        ('down', 'Menor es mejor'),
    ], string='Sentido de la meta', default='up', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsable', tracking=True)
    formula = fields.Text(string='Fórmula / Definición')
    active = fields.Boolean(default=True)
    value_ids = fields.One2many('hseq.indicator.value', 'indicator_id', string='Mediciones')
    last_value = fields.Float(string='Última medición', compute='_compute_last_value')

    def _compute_last_value(self):
        for rec in self:
            last = rec.value_ids.sorted('date', reverse=True)[:1]
            rec.last_value = last.value if last else 0.0


class HseqIndicatorValue(models.Model):
    _name = 'hseq.indicator.value'
    _description = 'Medición de Indicador HSEQ'
    _order = 'date desc, id desc'

    indicator_id = fields.Many2one(
        'hseq.indicator', string='Indicador', required=True, ondelete='cascade')
    site_id = fields.Many2one('hseq.site', string='Sede', index=True)
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today)
    value = fields.Float(string='Valor', required=True)
    target = fields.Float(
        string='Meta', compute='_compute_target', store=True, readonly=False)
    achieved = fields.Boolean(string='Meta cumplida', compute='_compute_achieved', store=True)
    notes = fields.Char(string='Observación')

    @api.depends('indicator_id')
    def _compute_target(self):
        for rec in self:
            if rec.indicator_id and not rec.target:
                rec.target = rec.indicator_id.target

    @api.depends('value', 'target', 'indicator_id.target_direction')
    def _compute_achieved(self):
        for rec in self:
            if rec.indicator_id.target_direction == 'down':
                rec.achieved = rec.value <= rec.target
            else:
                rec.achieved = rec.value >= rec.target
