# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqEppItem(models.Model):
    _name = 'hseq.epp.item'
    _description = 'Elemento de Protección Personal'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')
    category = fields.Selection([
        ('head', 'Protección de cabeza'),
        ('eyes', 'Protección visual'),
        ('ears', 'Protección auditiva'),
        ('respiratory', 'Protección respiratoria'),
        ('hands', 'Protección de manos'),
        ('feet', 'Protección de pies'),
        ('body', 'Protección corporal'),
        ('fall', 'Protección contra caídas'),
        ('other', 'Otro'),
    ], string='Categoría', default='other', required=True)
    lifespan_months = fields.Integer(string='Vida útil (meses)')
    description = fields.Text(string='Descripción / Norma técnica')
    active = fields.Boolean(default=True)


class HseqEppDelivery(models.Model):
    _name = 'hseq.epp.delivery'
    _description = 'Entrega de EPP'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today, tracking=True)
    employee_partner_id = fields.Many2one(
        'res.partner', string='Empleado', required=True, tracking=True)
    delivery_type = fields.Selection([
        ('delivery', 'Entrega'),
        ('return', 'Devolución'),
        ('replacement', 'Reposición'),
    ], string='Tipo', default='delivery', required=True, tracking=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsable de entrega', required=True,
        default=lambda self: self.env.user, tracking=True)
    line_ids = fields.One2many('hseq.epp.delivery.line', 'delivery_id', string='Elementos')
    accepted = fields.Boolean(string='Aceptado por el empleado', tracking=True)
    notes = fields.Text(string='Observaciones')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.epp.delivery') or self.env._('Nuevo')
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})


class HseqEppDeliveryLine(models.Model):
    _name = 'hseq.epp.delivery.line'
    _description = 'Línea de Entrega de EPP'

    delivery_id = fields.Many2one(
        'hseq.epp.delivery', string='Entrega', required=True, ondelete='cascade')
    item_id = fields.Many2one('hseq.epp.item', string='EPP', required=True)
    quantity = fields.Float(string='Cantidad', default=1.0, required=True)
    size = fields.Char(string='Talla')
    expiry_date = fields.Date(string='Vencimiento estimado')
    notes = fields.Char(string='Observación')
