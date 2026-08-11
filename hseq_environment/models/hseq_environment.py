# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqEnvironmentalAspect(models.Model):
    _name = 'hseq.environmental.aspect'
    _description = 'Aspecto e Impacto Ambiental'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'significance desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    aspect = fields.Char(string='Aspecto ambiental', required=True, tracking=True)
    impact = fields.Char(string='Impacto ambiental', required=True, tracking=True)
    aspect_type = fields.Selection([
        ('emission', 'Emisiones atmosféricas'),
        ('discharge', 'Vertimientos'),
        ('waste', 'Generación de residuos'),
        ('water', 'Consumo de agua'),
        ('energy', 'Consumo energético'),
        ('resources', 'Consumo de recursos'),
        ('spill', 'Derrames'),
        ('noise', 'Ruido'),
        ('other', 'Otro'),
    ], string='Tipo', default='other', required=True, tracking=True)
    condition = fields.Selection([
        ('normal', 'Normal'),
        ('abnormal', 'Anormal'),
        ('emergency', 'Emergencia'),
    ], string='Condición', default='normal', required=True)
    frequency = fields.Selection([
        ('1', 'Baja'), ('2', 'Media'), ('3', 'Alta'),
    ], string='Frecuencia', default='2', required=True)
    severity = fields.Selection([
        ('1', 'Baja'), ('2', 'Media'), ('3', 'Alta'),
    ], string='Severidad', default='2', required=True)
    significance = fields.Integer(
        string='Significancia', compute='_compute_significance', store=True)
    significant = fields.Boolean(
        string='Significativo', compute='_compute_significance', store=True)
    controls = fields.Text(string='Controles operacionales')
    responsible_id = fields.Many2one('res.users', string='Responsable', tracking=True)
    state = fields.Selection([
        ('draft', 'Identificado'),
        ('evaluated', 'Evaluado'),
        ('controlled', 'Controlado'),
        ('closed', 'Cerrado'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.environmental.aspect') or self.env._('Nuevo')
        return super().create(vals_list)

    @api.depends('frequency', 'severity')
    def _compute_significance(self):
        for rec in self:
            score = int(rec.frequency or 0) * int(rec.severity or 0)
            rec.significance = score
            rec.significant = score >= 6

    def action_evaluate(self):
        self.write({'state': 'evaluated'})

    def action_control(self):
        self.write({'state': 'controlled'})

    def action_close(self):
        self.write({'state': 'closed'})


class HseqConsumption(models.Model):
    _name = 'hseq.consumption'
    _description = 'Registro de Consumo Ambiental'
    _inherit = ['hseq.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Descripción')
    consumption_type = fields.Selection([
        ('water', 'Agua'),
        ('energy', 'Energía'),
        ('gas', 'Gas'),
        ('fuel', 'Combustible'),
        ('other', 'Otro'),
    ], string='Tipo', required=True, default='water')
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today)
    quantity = fields.Float(string='Cantidad', required=True)
    uom = fields.Char(string='Unidad', default='m³')
    notes = fields.Char(string='Observaciones')
