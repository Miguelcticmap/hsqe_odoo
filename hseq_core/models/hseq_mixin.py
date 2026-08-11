# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HseqMixin(models.AbstractModel):
    """Mixin transversal HSEQ.

    Aporta la jerarquía operativa de MAPEI Colombia:
    Sede -> Área -> Proceso -> Actividad
    a cualquier modelo del sistema HSEQ.
    """
    _name = 'hseq.mixin'
    _description = 'Mixin HSEQ (Sede / Área / Proceso / Actividad)'

    site_id = fields.Many2one(
        'hseq.site', string='Sede', index=True, ondelete='restrict')
    area_id = fields.Many2one(
        'hseq.area', string='Área', index=True, ondelete='restrict',
        domain="[('site_id', '=', site_id)]")
    process_id = fields.Many2one(
        'hseq.process', string='Proceso', index=True, ondelete='restrict',
        domain="[('area_id', '=', area_id)]")
    activity_id = fields.Many2one(
        'hseq.activity', string='Actividad', ondelete='restrict',
        domain="[('process_id', '=', process_id)]")

    @api.onchange('site_id')
    def _onchange_hseq_site_id(self):
        for rec in self:
            if rec.area_id and rec.area_id.site_id != rec.site_id:
                rec.area_id = False

    @api.onchange('area_id')
    def _onchange_hseq_area_id(self):
        for rec in self:
            if rec.area_id and not rec.site_id:
                rec.site_id = rec.area_id.site_id
            if rec.process_id and rec.process_id.area_id != rec.area_id:
                rec.process_id = False

    @api.onchange('process_id')
    def _onchange_hseq_process_id(self):
        for rec in self:
            if rec.process_id and not rec.area_id:
                rec.area_id = rec.process_id.area_id
                rec.site_id = rec.process_id.site_id
            if rec.activity_id and rec.activity_id.process_id != rec.process_id:
                rec.activity_id = False
