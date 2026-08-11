# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqDashboard(models.TransientModel):
    _name = 'hseq.dashboard'
    _description = 'Dashboard HSEQ MAPEI'

    site_id = fields.Many2one(
        'hseq.site', string='Sede',
        help='Deje vacío para consolidar todas las sedes.')
    accident_count = fields.Integer(string='Accidentes', compute='_compute_kpis')
    incident_count = fields.Integer(string='Incidentes', compute='_compute_kpis')
    near_miss_count = fields.Integer(string='Casi accidentes', compute='_compute_kpis')
    critical_risk_count = fields.Integer(string='Riesgos críticos', compute='_compute_kpis')
    open_nc_count = fields.Integer(string='NC abiertas', compute='_compute_kpis')
    overdue_action_count = fields.Integer(string='Acciones vencidas', compute='_compute_kpis')
    pending_inspection_count = fields.Integer(
        string='Inspecciones pendientes', compute='_compute_kpis')
    action_compliance = fields.Float(
        string='Cumplimiento de acciones (%)', compute='_compute_kpis')

    def _site_domain(self):
        self.ensure_one()
        return [('site_id', '=', self.site_id.id)] if self.site_id else []

    @api.depends('site_id')
    def _compute_kpis(self):
        for rec in self:
            dom = rec._site_domain()
            Incident = self.env['hseq.incident']
            rec.accident_count = Incident.search_count(
                dom + [('incident_type', '=', 'accident'), ('state', '!=', 'closed')])
            rec.incident_count = Incident.search_count(
                dom + [('incident_type', '=', 'incident'), ('state', '!=', 'closed')])
            rec.near_miss_count = Incident.search_count(
                dom + [('incident_type', '=', 'near_miss'), ('state', '!=', 'closed')])
            rec.critical_risk_count = self.env['hseq.risk'].search_count(
                dom + [('residual_level', '=', 'critical'), ('state', '!=', 'closed')])
            rec.open_nc_count = self.env['hseq.nonconformity'].search_count(
                dom + [('state', '!=', 'closed')])
            Action = self.env['hseq.action.plan']
            rec.overdue_action_count = Action.search_count(
                dom + [('is_overdue', '=', True)])
            rec.pending_inspection_count = self.env['hseq.inspection'].search_count(
                dom + [('state', 'in', ('draft', 'in_progress'))])
            total_actions = Action.search_count(dom)
            closed_actions = Action.search_count(
                dom + [('state', 'in', ('verified', 'closed'))])
            rec.action_compliance = (
                100.0 * closed_actions / total_actions if total_actions else 100.0)

    def _open(self, model, name, domain, context=None):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': model,
            'view_mode': 'list,form',
            'domain': self._site_domain() + domain,
            'context': context or {},
        }

    def action_open_accidents(self):
        return self._open('hseq.incident', self.env._('Accidentes'),
                          [('incident_type', '=', 'accident')])

    def action_open_incidents(self):
        return self._open('hseq.incident', self.env._('Incidentes'),
                          [('incident_type', '=', 'incident')])

    def action_open_critical_risks(self):
        return self._open('hseq.risk', self.env._('Riesgos críticos'),
                          [('residual_level', '=', 'critical')])

    def action_open_nc(self):
        return self._open('hseq.nonconformity', self.env._('NC abiertas'),
                          [('state', '!=', 'closed')])

    def action_open_overdue_actions(self):
        return self._open('hseq.action.plan', self.env._('Acciones vencidas'),
                          [('is_overdue', '=', True)])

    def action_open_pending_inspections(self):
        return self._open('hseq.inspection', self.env._('Inspecciones pendientes'),
                          [('state', 'in', ('draft', 'in_progress'))])

    def action_refresh(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hseq.dashboard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'inline',
        }
