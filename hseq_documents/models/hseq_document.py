# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqDocumentType(models.Model):
    _name = 'hseq.document.type'
    _description = 'Tipo de Documento HSEQ'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    active = fields.Boolean(default=True)


class HseqDocument(models.Model):
    _name = 'hseq.document'
    _description = 'Documento HSEQ'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'code, version desc'

    name = fields.Char(string='Título', required=True, tracking=True)
    code = fields.Char(string='Código', required=True, tracking=True)
    document_type_id = fields.Many2one(
        'hseq.document.type', string='Tipo de documento', required=True, tracking=True)
    version = fields.Integer(string='Versión', default=1, required=True, tracking=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsable', required=True,
        default=lambda self: self.env.user, tracking=True)
    approver_id = fields.Many2one('res.users', string='Aprobador', tracking=True)
    date_issued = fields.Date(string='Fecha de emisión')
    date_approved = fields.Date(string='Fecha de aprobación', readonly=True, copy=False)
    date_expiry = fields.Date(string='Fecha de vencimiento', tracking=True)
    file = fields.Binary(string='Archivo', attachment=True)
    file_name = fields.Char(string='Nombre del archivo')
    description = fields.Text(string='Descripción')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('review', 'Revisión'),
        ('approval', 'Aprobación'),
        ('current', 'Vigente'),
        ('obsolete', 'Obsoleto'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)

    _sql_constraints = [
        ('code_version_uniq', 'unique(code, version)',
         'Ya existe un documento con este código y versión.'),
    ]

    def action_review(self):
        self.write({'state': 'review'})

    def action_approval(self):
        self.write({'state': 'approval'})

    def action_approve(self):
        for rec in self:
            # Marca obsoletas las versiones vigentes anteriores del mismo código
            previous = self.search([
                ('code', '=', rec.code),
                ('id', '!=', rec.id),
                ('state', '=', 'current'),
            ])
            previous.write({'state': 'obsolete'})
            rec.write({
                'state': 'current',
                'date_approved': fields.Date.context_today(rec),
                'approver_id': rec.approver_id.id or self.env.user.id,
            })

    def action_obsolete(self):
        self.write({'state': 'obsolete'})

    def action_new_version(self):
        self.ensure_one()
        new_doc = self.copy({
            'version': self.version + 1,
            'state': 'draft',
            'date_approved': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hseq.document',
            'res_id': new_doc.id,
            'view_mode': 'form',
        }
