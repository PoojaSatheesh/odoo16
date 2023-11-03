# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# from odoo import models, fields
#
#
# class ToleranceWizard(models.TransientModel):
#     _name = "wizard.view"
#     _description = "Warning Message"
#
#     name = fields.Text(default="This quantity cannot be transferred ", readonly=True)
#     accept_id = fields.Many2one('stock.picking')
#
#     def action_accept(self):
#         self.accept_id.button_validate(click=True)
#
#     def action_reject(self):
#         return True
