# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class WorkOrder(models.Model):
    _inherit = "sale.order.line"

    machines_id = fields.Many2one(string="Machine name", comodel_name="machine.list")
    materials_received = fields.Boolean(string="Materials Received",
                                        help="If materials are received check the box as true")
    delivery_date = fields.Date(string="Delivery Date")
