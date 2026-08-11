# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqNonconformity(models.Model):
    _name = 'hseq.nonconformity'
    _description = 'No Conformidad'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    title = fields.Char(string='Título', required=True, tracking=True)
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today, tracking=True)
    source = fields.Selection([
        ('audit', 'Auditoría'),
        ('inspection', 'Inspección'),
        ('incident', 'Incidente'),
        ('complaint', 'Queja'),
        ('risk', 'Riesgo'),
        ('requirement', 'Requisito'),
        ('process', 'Proceso'),
        ('document', 'Documento'),
        ('other', 'Otro'),
    ], string='Origen', default='other', required=True, tracking=True)
    nc_type = fields.Selection([
        ('minor', 'Menor'),
        ('major', 'Mayor'),
        ('observation', 'Observación'),
        ('opportunity', 'Oportunidad de mejora'),
    ], string='Clasificación', default='minor', required=True, tracking=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsable', required=True,
        default=lambda self: self.env.user, tracking=True)
    description = fields.Html(string='Descripción')
    root_cause = fields.Text(string='Análisis de causa')
    correction = fields.Text(string='Corrección inmediata')
    state = fields.Selection([
        ('new', 'Nueva'),
        ('analysis', 'Análisis'),
        ('correction', 'Corrección'),
        ('corrective_action', 'Acción correctiva'),
        ('implementation', 'Implementación'),
        ('verification', 'Verificación'),
        ('closed', 'Cerrada'),
    ], string='Estado', default='new', required=True, tracking=True, copy=False)
    action_plan_ids = fields.One2many(
        'hseq.action.plan', 'nonconformity_id', string='Acciones correctivas')
    action_plan_count = fields.Integer(compute='_compute_action_plan_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.nonconformity') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_action_plan_count(self):
        for rec in self:
            rec.action_plan_count = len(rec.action_plan_ids)

    def action_analysis(self):
        self.write({'state': 'analysis'})

    def action_correction(self):
        self.write({'state': 'correction'})

    def action_corrective(self):
        self.write({'state': 'corrective_action'})

    def action_implementation(self):
        self.write({'state': 'implementation'})

    def action_verification(self):
        self.write({'state': 'verification'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_view_action_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Acciones correctivas'),
            'res_model': 'hseq.action.plan',
            'view_mode': 'list,form',
            'domain': [('nonconformity_id', '=', self.id)],
            'context': {
                'default_nonconformity_id': self.id,
                'default_origin': 'nonconformity',
                'default_origin_reference': self.name,
                'default_site_id': self.site_id.id,
                'default_area_id': self.area_id.id,
                'default_process_id': self.process_id.id,
            },
        }


class HseqActionPlanNonconformity(models.Model):
    _inherit = 'hseq.action.plan'

    nonconformity_id = fields.Many2one(
        'hseq.nonconformity', string='No conformidad', ondelete='set null')
