# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    tolerance = fields.Integer('Tolerance',
                               help='Give the tolerance number',
                               compute='_compute_tolerance',
                               inverse='_inverse_tolerance')

    # related='move_line_ids.tolerance')
    # compute='_compute_tolerance_in_delivery')

    @api.depends('sale_line_id.tolerance')
    def _compute_tolerance(self):
        for move in self:
            if move.sale_line_id:
                move.tolerance = move.sale_line_id.tolerance

    def _inverse_tolerance(self):
        for move in self:
            if move.sale_line_id:
                move.sale_line_id.tolerance = move.tolerance
