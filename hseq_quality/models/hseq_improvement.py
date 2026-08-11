# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqImprovement(models.Model):
    _name = 'hseq.improvement'
    _description = 'Oportunidad de Mejora'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    title = fields.Char(string='Título', required=True, tracking=True)
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today)
    proposed_by_id = fields.Many2one(
        'res.users', string='Propuesta por', default=lambda self: self.env.user)
    responsible_id = fields.Many2one('res.users', string='Responsable', tracking=True)
    description = fields.Html(string='Descripción')
    expected_benefit = fields.Text(string='Beneficio esperado')
    state = fields.Selection([
        ('draft', 'Propuesta'),
        ('evaluation', 'Evaluación'),
        ('approved', 'Aprobada'),
        ('implementation', 'Implementación'),
        ('done', 'Implementada'),
        ('rejected', 'Rechazada'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.improvement') or self.env._('Nuevo')
        return super().create(vals_list)

    def action_evaluate(self):
        self.write({'state': 'evaluation'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_implement(self):
        self.write({'state': 'implementation'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_reject(self):
        self.write({'state': 'rejected'})
