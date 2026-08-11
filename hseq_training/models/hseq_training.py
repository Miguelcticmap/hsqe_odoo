# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqTrainingCourse(models.Model):
    _name = 'hseq.training.course'
    _description = 'Curso de Capacitación'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    duration_hours = fields.Float(string='Duración (horas)')
    validity_months = fields.Integer(
        string='Vigencia (meses)',
        help='Vigencia del certificado. 0 = sin vencimiento.')
    mandatory = fields.Boolean(string='Obligatorio')
    description = fields.Text(string='Contenido')
    active = fields.Boolean(default=True)


class HseqTrainingSession(models.Model):
    _name = 'hseq.training.session'
    _description = 'Sesión de Capacitación'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    course_id = fields.Many2one(
        'hseq.training.course', string='Curso', required=True, tracking=True)
    date = fields.Datetime(string='Fecha programada', required=True, tracking=True)
    trainer = fields.Char(string='Facilitador')
    trainer_partner_id = fields.Many2one('res.partner', string='Facilitador (contacto)')
    target = fields.Selection([
        ('company', 'Toda MAPEI'),
        ('site', 'Una sede'),
        ('area', 'Un área'),
        ('process', 'Un proceso'),
        ('job', 'Un cargo'),
        ('group', 'Grupo de empleados'),
    ], string='Dirigido a', default='group', required=True)
    attendee_ids = fields.One2many(
        'hseq.training.attendee', 'session_id', string='Participantes')
    attendee_count = fields.Integer(compute='_compute_attendee_stats')
    attendance_rate = fields.Float(
        string='% Asistencia', compute='_compute_attendee_stats')
    notes = fields.Text(string='Observaciones')
    state = fields.Selection([
        ('planned', 'Programada'),
        ('done', 'Ejecutada'),
        ('cancelled', 'Cancelada'),
    ], string='Estado', default='planned', required=True, tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.training.session') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_attendee_stats(self):
        for rec in self:
            total = len(rec.attendee_ids)
            rec.attendee_count = total
            rec.attendance_rate = (
                100.0 * len(rec.attendee_ids.filtered('attended')) / total
                if total else 0.0)

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_replan(self):
        self.write({'state': 'planned'})


class HseqTrainingAttendee(models.Model):
    _name = 'hseq.training.attendee'
    _description = 'Participante de Capacitación'

    session_id = fields.Many2one(
        'hseq.training.session', string='Sesión', required=True, ondelete='cascade')
    partner_id = fields.Many2one(
        'res.partner', string='Participante', required=True)
    attended = fields.Boolean(string='Asistió')
    score = fields.Float(string='Calificación')
    passed = fields.Boolean(string='Aprobó')
    certificate_expiry = fields.Date(string='Vencimiento certificado')
    notes = fields.Char(string='Observación')
