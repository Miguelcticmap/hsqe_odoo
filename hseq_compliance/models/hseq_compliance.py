# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqLegalRequirement(models.Model):
    _name = 'hseq.legal.requirement'
    _description = 'Requisito Legal HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date_deadline asc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    title = fields.Char(string='Requisito / Norma', required=True, tracking=True)
    authority = fields.Char(string='Entidad emisora')
    domain_type = fields.Selection([
        ('sst', 'SST'),
        ('environment', 'Ambiental'),
        ('quality', 'Calidad'),
        ('general', 'General'),
    ], string='Dominio', default='general', required=True, tracking=True)
    obligation = fields.Text(string='Obligación', required=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsable', required=True,
        default=lambda self: self.env.user, tracking=True)
    periodicity = fields.Selection([
        ('once', 'Única vez'),
        ('monthly', 'Mensual'),
        ('quarterly', 'Trimestral'),
        ('semiannual', 'Semestral'),
        ('annual', 'Anual'),
        ('permanent', 'Permanente'),
    ], string='Periodicidad', default='annual', tracking=True)
    date_deadline = fields.Date(string='Fecha límite', tracking=True)
    evidence = fields.Text(string='Evidencia de cumplimiento')
    compliance_state = fields.Selection([
        ('pending', 'Pendiente'),
        ('in_progress', 'En gestión'),
        ('compliant', 'Cumplido'),
        ('non_compliant', 'Incumplido'),
        ('not_applicable', 'No aplica'),
    ], string='Estado de cumplimiento', default='pending',
        required=True, tracking=True, copy=False)
    is_overdue = fields.Boolean(
        string='Vencido', compute='_compute_is_overdue', search='_search_is_overdue')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.legal.requirement') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_overdue = bool(
                rec.date_deadline and rec.date_deadline < today
                and rec.compliance_state in ('pending', 'in_progress'))

    def _search_is_overdue(self, operator, value):
        today = fields.Date.context_today(self)
        domain = [
            ('date_deadline', '<', today),
            ('compliance_state', 'in', ('pending', 'in_progress')),
        ]
        if (operator == '=' and value) or (operator == '!=' and not value):
            return domain
        return ['!'] + domain

    def action_in_progress(self):
        self.write({'compliance_state': 'in_progress'})

    def action_compliant(self):
        self.write({'compliance_state': 'compliant'})

    def action_non_compliant(self):
        self.write({'compliance_state': 'non_compliant'})
