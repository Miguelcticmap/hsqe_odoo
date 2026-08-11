# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqContractor(models.Model):
    _name = 'hseq.contractor'
    _description = 'Contratista HSEQ'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    partner_id = fields.Many2one(
        'res.partner', string='Empresa contratista', required=True, tracking=True)
    service = fields.Char(string='Servicio contratado', tracking=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsable HSEQ',
        default=lambda self: self.env.user, tracking=True)
    site_ids = fields.Many2many(
        'hseq.site', 'hseq_contractor_site_rel', 'contractor_id', 'site_id',
        string='Sedes autorizadas', tracking=True)
    document_ids = fields.One2many(
        'hseq.contractor.document', 'contractor_id', string='Documentación')
    worker_ids = fields.One2many(
        'hseq.contractor.worker', 'contractor_id', string='Personal')
    induction_done = fields.Boolean(string='Inducción realizada', tracking=True)
    induction_date = fields.Date(string='Fecha de inducción')
    notes = fields.Text(string='Observaciones')
    state = fields.Selection([
        ('pending', 'Pendiente'),
        ('review', 'En revisión'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('expired', 'Vencido'),
        ('blocked', 'Bloqueado'),
    ], string='Estado', default='pending', required=True, tracking=True, copy=False)
    expired_doc_count = fields.Integer(
        string='Docs vencidos', compute='_compute_expired_doc_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.contractor') or self.env._('Nuevo')
        return super().create(vals_list)

    def _compute_expired_doc_count(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.expired_doc_count = len(rec.document_ids.filtered(
                lambda d: d.date_expiry and d.date_expiry < today))

    def action_review(self):
        self.write({'state': 'review'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def action_block(self):
        self.write({'state': 'blocked'})

    def action_reset(self):
        self.write({'state': 'pending'})


class HseqContractorDocument(models.Model):
    _name = 'hseq.contractor.document'
    _description = 'Documento de Contratista'
    _order = 'date_expiry'

    contractor_id = fields.Many2one(
        'hseq.contractor', string='Contratista', required=True, ondelete='cascade')
    name = fields.Char(string='Documento / Certificación', required=True)
    file = fields.Binary(string='Archivo', attachment=True)
    file_name = fields.Char(string='Nombre archivo')
    date_expiry = fields.Date(string='Vencimiento')
    valid = fields.Boolean(string='Vigente', compute='_compute_valid')
    notes = fields.Char(string='Observación')

    def _compute_valid(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.valid = not rec.date_expiry or rec.date_expiry >= today


class HseqContractorWorker(models.Model):
    _name = 'hseq.contractor.worker'
    _description = 'Trabajador de Contratista'

    contractor_id = fields.Many2one(
        'hseq.contractor', string='Contratista', required=True, ondelete='cascade')
    name = fields.Char(string='Nombre', required=True)
    identification = fields.Char(string='Identificación')
    role = fields.Char(string='Cargo')
    arl_ok = fields.Boolean(string='ARL vigente')
    social_security_ok = fields.Boolean(string='Seguridad social vigente')
    induction_done = fields.Boolean(string='Inducción')
