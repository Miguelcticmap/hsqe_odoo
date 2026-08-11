# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqWasteType(models.Model):
    _name = 'hseq.waste.type'
    _description = 'Tipo de Residuo'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    classification = fields.Selection([
        ('ordinary', 'Ordinario'),
        ('recyclable', 'Aprovechable'),
        ('organic', 'Orgánico'),
        ('hazardous', 'Peligroso'),
        ('special', 'Especial'),
        ('rcd', 'RCD'),
    ], string='Clasificación', required=True, default='ordinary')
    active = fields.Boolean(default=True)


class HseqWasteRecord(models.Model):
    _name = 'hseq.waste.record'
    _description = 'Registro de Residuo'
    _inherit = ['hseq.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Referencia', required=True, copy=False, readonly=True,
        default=lambda self: self.env._('Nuevo'))
    waste_type_id = fields.Many2one(
        'hseq.waste.type', string='Tipo de residuo', required=True, tracking=True)
    classification = fields.Selection(
        related='waste_type_id.classification', string='Clasificación', store=True)
    date = fields.Date(
        string='Fecha', required=True, default=fields.Date.context_today, tracking=True)
    quantity = fields.Float(string='Cantidad', required=True, tracking=True)
    uom = fields.Char(string='Unidad', default='kg', required=True)
    manager_partner_id = fields.Many2one(
        'res.partner', string='Gestor de residuos', tracking=True)
    disposal_method = fields.Selection([
        ('recycling', 'Reciclaje'),
        ('landfill', 'Relleno sanitario'),
        ('incineration', 'Incineración'),
        ('treatment', 'Tratamiento'),
        ('reuse', 'Reutilización'),
        ('other', 'Otro'),
    ], string='Método de disposición', tracking=True)
    certificate = fields.Char(string='Certificado de disposición')
    notes = fields.Text(string='Observaciones')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('disposed', 'Dispuesto'),
    ], string='Estado', default='draft', required=True, tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', self.env._('Nuevo')) == self.env._('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hseq.waste.record') or self.env._('Nuevo')
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_dispose(self):
        self.write({'state': 'disposed'})
