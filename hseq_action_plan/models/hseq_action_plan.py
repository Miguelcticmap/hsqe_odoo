# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqActionPlan(models.Model):
    _name = 'hseq.action.plan'
    _description = 'Plan de Acción HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date_deadline asc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    description = fields.Char(string='Acción', required=True, tracking=True)
    detail = fields.Html(string='Detalle')
    action_type = fields.Selection([
        ('corrective', 'Correctiva'),
        ('preventive', 'Preventiva'),
        ('improvement', 'Mejora'),
        ('correction', 'Corrección inmediata'),
    ], string='Tipo de acción', default='corrective', required=True, tracking=True)
    origin = fields.Selection([
        ('incident', 'Incidente'),
        ('inspection', 'Inspección'),
        ('audit', 'Auditoría'),
        ('nonconformity', 'No conformidad'),
        ('risk', 'Riesgo'),
        ('compliance', 'Compliance'),
        ('complaint', 'Queja'),
        ('other', 'Otro'),
    ], string='Origen', default='other', tracking=True)
    origin_reference = fields.Char(string='Referencia de origen')
    responsible_id = fields.Many2one(
        'res.users', string='Responsable', required=True, tracking=True,
        default=lambda self: self.env.user)
    verifier_id = fields.Many2one('res.users', string='Verificador', tracking=True)
    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
        ('3', 'Crítica'),
    ], string='Prioridad', default='1', tracking=True)
    date_start = fields.Date(string='Fecha inicial', default=fields.Date.context_today)
    date_deadline = fields.Date(string='Fecha compromiso', tracking=True)
    date_closed = fields.Date(string='Fecha de cierre', readonly=True, copy=False)
    progress = fields.Integer(string='Avance (%)', tracking=True)
    effectiveness = fields.Selection([
        ('effective', 'Eficaz'),
        ('not_effective', 'No eficaz'),
        ('pending', 'Pendiente de evaluación'),
    ], string='Evaluación de eficacia', default='pending', tracking=True)
    effectiveness_notes = fields.Text(string='Observaciones de eficacia')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En ejecución'),
        ('done', 'Ejecutada'),
        ('verified', 'Verificada'),
        ('closed', 'Cerrada'),
        ('cancelled', 'Cancelada'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)
    is_overdue = fields.Boolean(
        string='Vencida', compute='_compute_is_overdue', search='_search_is_overdue')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.action.plan') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_overdue = bool(
                rec.date_deadline
                and rec.date_deadline < today
                and rec.state in ('draft', 'in_progress'))

    def _search_is_overdue(self, operator, value):
        today = fields.Date.context_today(self)
        domain = [
            ('date_deadline', '<', today),
            ('state', 'in', ('draft', 'in_progress')),
        ]
        if (operator == '=' and value) or (operator == '!=' and not value):
            return domain
        return ['!'] + domain

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done', 'progress': 100})

    def action_verify(self):
        self.write({'state': 'verified'})

    def action_close(self):
        self.write({
            'state': 'closed',
            'date_closed': fields.Date.context_today(self),
        })

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft', 'date_closed': False})
