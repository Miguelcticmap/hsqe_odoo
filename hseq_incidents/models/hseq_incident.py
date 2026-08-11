# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqIncident(models.Model):
    _name = 'hseq.incident'
    _description = 'Incidente / Accidente HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    title = fields.Char(string='Título', required=True, tracking=True)
    incident_type = fields.Selection([
        ('incident', 'Incidente'),
        ('accident', 'Accidente'),
        ('near_miss', 'Casi accidente'),
        ('unsafe_condition', 'Condición insegura'),
        ('unsafe_act', 'Acto inseguro'),
    ], string='Tipo', required=True, default='incident', tracking=True)
    severity = fields.Selection([
        ('minor', 'Leve'),
        ('moderate', 'Moderado'),
        ('serious', 'Grave'),
        ('fatal', 'Mortal'),
    ], string='Severidad', default='minor', tracking=True)
    date = fields.Datetime(
        string='Fecha y hora', required=True,
        default=fields.Datetime.now, tracking=True)
    reported_by_id = fields.Many2one(
        'res.users', string='Reportado por', required=True,
        default=lambda self: self.env.user, tracking=True)
    involved_partner_id = fields.Many2one(
        'res.partner', string='Persona involucrada', tracking=True)
    involved_name = fields.Char(string='Nombre involucrado (texto)')
    witness_ids = fields.Many2many(
        'res.partner', 'hseq_incident_witness_rel', 'incident_id', 'partner_id',
        string='Testigos')
    description = fields.Html(string='Descripción de los hechos')
    lost_days = fields.Integer(string='Días perdidos')
    with_injury = fields.Boolean(string='Con lesión')
    body_part = fields.Char(string='Parte del cuerpo afectada')

    investigator_id = fields.Many2one('res.users', string='Investigador', tracking=True)
    root_cause = fields.Text(string='Análisis causal / Causa raíz')
    immediate_cause = fields.Text(string='Causas inmediatas')
    basic_cause = fields.Text(string='Causas básicas')

    state = fields.Selection([
        ('reported', 'Reportado'),
        ('investigation', 'Investigación'),
        ('analysis', 'Análisis causal'),
        ('action_plan', 'Plan de acción'),
        ('follow_up', 'Seguimiento'),
        ('verification', 'Verificación'),
        ('closed', 'Cerrado'),
    ], string='Estado', default='reported', required=True, tracking=True, copy=False)

    action_plan_ids = fields.One2many(
        'hseq.action.plan', 'incident_id', string='Planes de acción')
    action_plan_count = fields.Integer(compute='_compute_action_plan_count')
    attachment_count = fields.Integer(compute='_compute_attachment_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.incident') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_action_plan_count(self):
        for rec in self:
            rec.action_plan_count = len(rec.action_plan_ids)

    def _compute_attachment_count(self):
        data = self.env['ir.attachment']._read_group(
            [('res_model', '=', self._name), ('res_id', 'in', self.ids)],
            ['res_id'], ['__count'])
        counts = {res_id: count for res_id, count in data}
        for rec in self:
            rec.attachment_count = counts.get(rec.id, 0)

    def action_start_investigation(self):
        self.write({'state': 'investigation'})

    def action_analysis(self):
        self.write({'state': 'analysis'})

    def action_action_plan(self):
        self.write({'state': 'action_plan'})

    def action_follow_up(self):
        self.write({'state': 'follow_up'})

    def action_verification(self):
        self.write({'state': 'verification'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_view_action_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Planes de acción'),
            'res_model': 'hseq.action.plan',
            'view_mode': 'list,form',
            'domain': [('incident_id', '=', self.id)],
            'context': {
                'default_incident_id': self.id,
                'default_origin': 'incident',
                'default_origin_reference': self.name,
                'default_site_id': self.site_id.id,
                'default_area_id': self.area_id.id,
                'default_process_id': self.process_id.id,
            },
        }

    def action_view_attachments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Evidencias'),
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,list,form',
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'context': {'default_res_model': self._name, 'default_res_id': self.id},
        }


class HseqActionPlanIncident(models.Model):
    _inherit = 'hseq.action.plan'

    incident_id = fields.Many2one(
        'hseq.incident', string='Incidente', ondelete='set null')
