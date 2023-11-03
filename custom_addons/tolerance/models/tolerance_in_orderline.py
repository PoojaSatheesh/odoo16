# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tolerance = fields.Integer('Tolerance',
                               help='Give the tolerance number', compute='_compute_tolerance',
                               inverse='_inverse_tolerance')

    @api.depends('order_id.partner_id.tolerance')
    def _compute_tolerance(self):
        for line in self:
            line.tolerance = line.order_id.partner_id.tolerance

    def _inverse_tolerance(self):
        for line in self:
            line.order_id.partner_id.tolerance = line.tolerance
