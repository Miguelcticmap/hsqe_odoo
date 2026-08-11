# -*- coding: utf-8 -*-
from odoo import api, fields, models

RISK_LEVELS = [
    ('low', 'Bajo'),
    ('medium', 'Medio'),
    ('high', 'Alto'),
    ('critical', 'Crítico'),
]


class HseqHazardType(models.Model):
    _name = 'hseq.hazard.type'
    _description = 'Tipo de Peligro'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    description = fields.Text(string='Descripción')
    active = fields.Boolean(default=True)


class HseqRisk(models.Model):
    _name = 'hseq.risk'
    _description = 'Riesgo HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'residual_score desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    hazard_type_id = fields.Many2one(
        'hseq.hazard.type', string='Tipo de peligro', required=True, tracking=True)
    hazard_description = fields.Char(string='Peligro', required=True, tracking=True)
    risk_description = fields.Text(string='Descripción del riesgo')
    domain_type = fields.Selection([
        ('sst', 'SST'),
        ('quality', 'Calidad'),
        ('environment', 'Ambiental'),
        ('process', 'Proceso'),
    ], string='Dominio', default='sst', required=True, tracking=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsable', tracking=True,
        default=lambda self: self.env.user)

    probability = fields.Selection([
        ('1', 'Rara'), ('2', 'Improbable'), ('3', 'Posible'),
        ('4', 'Probable'), ('5', 'Casi segura'),
    ], string='Probabilidad', default='3', required=True, tracking=True)
    severity = fields.Selection([
        ('1', 'Insignificante'), ('2', 'Menor'), ('3', 'Moderada'),
        ('4', 'Mayor'), ('5', 'Catastrófica'),
    ], string='Severidad', default='3', required=True, tracking=True)
    inherent_score = fields.Integer(
        string='Puntaje inherente', compute='_compute_inherent', store=True)
    inherent_level = fields.Selection(
        RISK_LEVELS, string='Riesgo inherente',
        compute='_compute_inherent', store=True, tracking=True)

    control_ids = fields.One2many('hseq.risk.control', 'risk_id', string='Controles')

    residual_probability = fields.Selection([
        ('1', 'Rara'), ('2', 'Improbable'), ('3', 'Posible'),
        ('4', 'Probable'), ('5', 'Casi segura'),
    ], string='Probabilidad residual', default='3', required=True, tracking=True)
    residual_severity = fields.Selection([
        ('1', 'Insignificante'), ('2', 'Menor'), ('3', 'Moderada'),
        ('4', 'Mayor'), ('5', 'Catastrófica'),
    ], string='Severidad residual', default='3', required=True, tracking=True)
    residual_score = fields.Integer(
        string='Puntaje residual', compute='_compute_residual', store=True)
    residual_level = fields.Selection(
        RISK_LEVELS, string='Riesgo residual',
        compute='_compute_residual', store=True, tracking=True)

    review_date = fields.Date(string='Próxima revisión', tracking=True)
    state = fields.Selection([
        ('draft', 'Identificado'),
        ('evaluated', 'Evaluado'),
        ('controlled', 'Controlado'),
        ('review', 'En revisión'),
        ('closed', 'Cerrado'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)
    action_plan_ids = fields.One2many(
        'hseq.action.plan', 'risk_id', string='Planes de acción')
    action_plan_count = fields.Integer(compute='_compute_action_plan_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.risk') or self.env._('Nuevo')
        return super().create(vals_list)

    @staticmethod
    def _score_to_level(score):
        if score <= 4:
            return 'low'
        if score <= 9:
            return 'medium'
        if score <= 15:
            return 'high'
        return 'critical'

    @api.depends('probability', 'severity')
    def _compute_inherent(self):
        for rec in self:
            score = int(rec.probability or 0) * int(rec.severity or 0)
            rec.inherent_score = score
            rec.inherent_level = self._score_to_level(score) if score else False

    @api.depends('residual_probability', 'residual_severity')
    def _compute_residual(self):
        for rec in self:
            score = int(rec.residual_probability or 0) * int(rec.residual_severity or 0)
            rec.residual_score = score
            rec.residual_level = self._score_to_level(score) if score else False

    def _compute_action_plan_count(self):
        for rec in self:
            rec.action_plan_count = len(rec.action_plan_ids)

    def action_evaluate(self):
        self.write({'state': 'evaluated'})

    def action_control(self):
        self.write({'state': 'controlled'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_view_action_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Planes de acción'),
            'res_model': 'hseq.action.plan',
            'view_mode': 'list,form',
            'domain': [('risk_id', '=', self.id)],
            'context': {
                'default_risk_id': self.id,
                'default_origin': 'risk',
                'default_origin_reference': self.name,
                'default_site_id': self.site_id.id,
                'default_area_id': self.area_id.id,
                'default_process_id': self.process_id.id,
            },
        }


class HseqRiskControl(models.Model):
    _name = 'hseq.risk.control'
    _description = 'Control de Riesgo'
    _order = 'risk_id, sequence, id'

    sequence = fields.Integer(default=10)
    risk_id = fields.Many2one(
        'hseq.risk', string='Riesgo', required=True, ondelete='cascade')
    name = fields.Char(string='Control', required=True)
    control_type = fields.Selection([
        ('elimination', 'Eliminación'),
        ('substitution', 'Sustitución'),
        ('engineering', 'Control de ingeniería'),
        ('administrative', 'Control administrativo'),
        ('epp', 'EPP'),
    ], string='Jerarquía de control', required=True, default='administrative')
    responsible_id = fields.Many2one('res.users', string='Responsable')
    effective = fields.Boolean(string='Eficaz')
    notes = fields.Char(string='Observaciones')


class HseqActionPlanRisk(models.Model):
    _inherit = 'hseq.action.plan'

    risk_id = fields.Many2one('hseq.risk', string='Riesgo', ondelete='set null')
