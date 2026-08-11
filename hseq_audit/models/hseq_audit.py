# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqAudit(models.Model):
    _name = 'hseq.audit'
    _description = 'Auditoría HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    title = fields.Char(string='Título', required=True, tracking=True)
    audit_type = fields.Selection([
        ('internal', 'Interna'),
        ('external', 'Externa'),
        ('process', 'De proceso'),
        ('hseq', 'HSEQ'),
        ('supplier', 'De proveedor'),
    ], string='Tipo', default='internal', required=True, tracking=True)
    standard = fields.Char(
        string='Norma / Criterio', help='Ej: ISO 9001, ISO 14001, ISO 45001')
    date_start = fields.Date(string='Fecha inicio', tracking=True)
    date_end = fields.Date(string='Fecha fin', tracking=True)
    lead_auditor_id = fields.Many2one(
        'res.users', string='Auditor líder', required=True,
        default=lambda self: self.env.user, tracking=True)
    auditor_ids = fields.Many2many(
        'res.users', 'hseq_audit_auditor_rel', 'audit_id', 'user_id',
        string='Equipo auditor')
    audited_partner_id = fields.Many2one(
        'res.partner', string='Auditado (externo/proveedor)')
    scope = fields.Text(string='Alcance')
    objective = fields.Text(string='Objetivo')
    conclusions = fields.Html(string='Conclusiones / Informe')
    state = fields.Selection([
        ('planned', 'Planificación'),
        ('preparation', 'Preparación'),
        ('execution', 'Ejecución'),
        ('report', 'Informe'),
        ('follow_up', 'Seguimiento'),
        ('closed', 'Cerrada'),
    ], string='Estado', default='planned', required=True, tracking=True, copy=False)
    finding_ids = fields.One2many('hseq.audit.finding', 'audit_id', string='Hallazgos')
    finding_count = fields.Integer(compute='_compute_counts')
    action_plan_ids = fields.One2many(
        'hseq.action.plan', 'audit_id', string='Planes de acción')
    action_plan_count = fields.Integer(compute='_compute_counts')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.audit') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_counts(self):
        for rec in self:
            rec.finding_count = len(rec.finding_ids)
            rec.action_plan_count = len(rec.action_plan_ids)

    def action_preparation(self):
        self.write({'state': 'preparation'})

    def action_execution(self):
        self.write({'state': 'execution'})

    def action_report(self):
        self.write({'state': 'report'})

    def action_follow_up(self):
        self.write({'state': 'follow_up'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_view_action_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Planes de acción'),
            'res_model': 'hseq.action.plan',
            'view_mode': 'list,form',
            'domain': [('audit_id', '=', self.id)],
            'context': {
                'default_audit_id': self.id,
                'default_origin': 'audit',
                'default_origin_reference': self.name,
                'default_site_id': self.site_id.id,
            },
        }


class HseqAuditFinding(models.Model):
    _name = 'hseq.audit.finding'
    _description = 'Hallazgo de Auditoría'
    _order = 'audit_id, sequence, id'

    sequence = fields.Integer(default=10)
    audit_id = fields.Many2one(
        'hseq.audit', string='Auditoría', required=True, ondelete='cascade')
    name = fields.Char(string='Hallazgo', required=True)
    finding_type = fields.Selection([
        ('nc_major', 'No conformidad mayor'),
        ('nc_minor', 'No conformidad menor'),
        ('observation', 'Observación'),
        ('opportunity', 'Oportunidad de mejora'),
        ('strength', 'Fortaleza'),
    ], string='Tipo', default='observation', required=True)
    criterion = fields.Char(string='Criterio / Cláusula')
    evidence = fields.Text(string='Evidencia')
    nonconformity_id = fields.Many2one(
        'hseq.nonconformity', string='No conformidad generada', readonly=True)

    def action_create_nonconformity(self):
        for finding in self:
            if finding.nonconformity_id:
                continue
            nc = self.env['hseq.nonconformity'].create({
                'title': finding.name,
                'source': 'audit',
                'nc_type': 'major' if finding.finding_type == 'nc_major' else 'minor',
                'site_id': finding.audit_id.site_id.id,
                'area_id': finding.audit_id.area_id.id,
                'process_id': finding.audit_id.process_id.id,
                'responsible_id': finding.audit_id.lead_auditor_id.id,
                'description': finding.evidence or '',
            })
            finding.nonconformity_id = nc


class HseqActionPlanAudit(models.Model):
    _inherit = 'hseq.action.plan'

    audit_id = fields.Many2one('hseq.audit', string='Auditoría', ondelete='set null')
