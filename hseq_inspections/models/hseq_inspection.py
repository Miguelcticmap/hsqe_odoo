# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqInspectionTemplate(models.Model):
    _name = 'hseq.inspection.template'
    _description = 'Plantilla de Inspección'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    active = fields.Boolean(default=True)
    description = fields.Text(string='Descripción')
    auto_create_action = fields.Boolean(
        string='Crear acción por respuesta negativa',
        help='Si está activo, al finalizar la inspección se crea automáticamente '
             'un plan de acción por cada pregunta que no cumple.')
    question_ids = fields.One2many(
        'hseq.inspection.template.question', 'template_id', string='Preguntas')


class HseqInspectionTemplateQuestion(models.Model):
    _name = 'hseq.inspection.template.question'
    _description = 'Pregunta de Plantilla de Inspección'
    _order = 'template_id, sequence, id'

    sequence = fields.Integer(default=10)
    template_id = fields.Many2one(
        'hseq.inspection.template', string='Plantilla',
        required=True, ondelete='cascade')
    name = fields.Char(string='Pregunta', required=True)
    answer_type = fields.Selection([
        ('compliance', 'Cumple / No cumple / No aplica'),
        ('numeric', 'Valor numérico'),
        ('text', 'Texto'),
    ], string='Tipo de respuesta', default='compliance', required=True)
    mandatory_evidence = fields.Boolean(string='Requiere evidencia')


class HseqInspection(models.Model):
    _name = 'hseq.inspection'
    _description = 'Inspección HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    template_id = fields.Many2one(
        'hseq.inspection.template', string='Plantilla', required=True, tracking=True)
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today, tracking=True)
    inspector_id = fields.Many2one(
        'res.users', string='Inspector', required=True,
        default=lambda self: self.env.user, tracking=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En ejecución'),
        ('done', 'Finalizada'),
        ('closed', 'Cerrada'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)
    line_ids = fields.One2many('hseq.inspection.line', 'inspection_id', string='Respuestas')
    notes = fields.Text(string='Observaciones')
    compliance_rate = fields.Float(
        string='% Cumplimiento', compute='_compute_compliance_rate', store=True)
    action_plan_ids = fields.One2many(
        'hseq.action.plan', 'inspection_id', string='Planes de acción')
    action_plan_count = fields.Integer(compute='_compute_action_plan_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.inspection') or self.env._('Nuevo')
        return super().create(vals_list)

    @api.depends('line_ids.answer')
    def _compute_compliance_rate(self):
        for rec in self:
            lines = rec.line_ids.filtered(
                lambda l: l.answer_type == 'compliance' and l.answer in ('yes', 'no'))
            total = len(lines)
            rec.compliance_rate = (
                100.0 * len(lines.filtered(lambda l: l.answer == 'yes')) / total
                if total else 0.0)

    def _compute_action_plan_count(self):
        for rec in self:
            rec.action_plan_count = len(rec.action_plan_ids)

    def action_start(self):
        for rec in self:
            if not rec.line_ids:
                rec.line_ids = [
                    (0, 0, {
                        'question_id': q.id,
                        'name': q.name,
                        'answer_type': q.answer_type,
                    }) for q in rec.template_id.question_ids
                ]
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            if rec.template_id.auto_create_action:
                for line in rec.line_ids.filtered(lambda l: l.answer == 'no'):
                    self.env['hseq.action.plan'].create({
                        'description': self.env._(
                            'Hallazgo inspección %(insp)s: %(question)s',
                            insp=rec.name, question=line.name),
                        'action_type': 'corrective',
                        'origin': 'inspection',
                        'origin_reference': rec.name,
                        'inspection_id': rec.id,
                        'site_id': rec.site_id.id,
                        'area_id': rec.area_id.id,
                        'process_id': rec.process_id.id,
                        'responsible_id': rec.inspector_id.id,
                    })

    def action_close(self):
        self.write({'state': 'closed'})

    def action_view_action_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.env._('Planes de acción'),
            'res_model': 'hseq.action.plan',
            'view_mode': 'list,form',
            'domain': [('inspection_id', '=', self.id)],
            'context': {
                'default_inspection_id': self.id,
                'default_origin': 'inspection',
                'default_origin_reference': self.name,
                'default_site_id': self.site_id.id,
            },
        }


class HseqInspectionLine(models.Model):
    _name = 'hseq.inspection.line'
    _description = 'Línea de Inspección'
    _order = 'inspection_id, sequence, id'

    sequence = fields.Integer(default=10)
    inspection_id = fields.Many2one(
        'hseq.inspection', string='Inspección', required=True, ondelete='cascade')
    question_id = fields.Many2one(
        'hseq.inspection.template.question', string='Pregunta plantilla')
    name = fields.Char(string='Pregunta', required=True)
    answer_type = fields.Selection([
        ('compliance', 'Cumple / No cumple / No aplica'),
        ('numeric', 'Valor numérico'),
        ('text', 'Texto'),
    ], string='Tipo', default='compliance', required=True)
    answer = fields.Selection([
        ('yes', 'Cumple'),
        ('no', 'No cumple'),
        ('na', 'No aplica'),
    ], string='Respuesta')
    value_numeric = fields.Float(string='Valor')
    value_text = fields.Char(string='Texto')
    comments = fields.Char(string='Observación')


class HseqActionPlanInspection(models.Model):
    _inherit = 'hseq.action.plan'

    inspection_id = fields.Many2one(
        'hseq.inspection', string='Inspección', ondelete='set null')
