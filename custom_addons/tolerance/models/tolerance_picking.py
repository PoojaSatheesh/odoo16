# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self, click=False):
        min_acceptable = self.move_ids_without_package.tolerance - self.move_ids_without_package.product_uom_qty
        max_acceptable = self.move_ids_without_package.tolerance + self.move_ids_without_package.product_uom_qty

        if click == True:
            return super().button_validate()

        elif (self.move_ids_without_package.quantity_done < abs(min_acceptable) or
              self.move_ids_without_package.quantity_done > max_acceptable):

            return {
                'name': "Test Wizard",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.view',
                'view_id': self.env.ref('tolerance.tolerance_wizard_view_form').id,
                'context': {'default_accept': self.id},
                'target': 'new',
            }
        else:
            return super().button_validate()


class ToleranceWizard(models.TransientModel):
    _name = "wizard.view"
    _description = "Warning Message"

    name = fields.Text(default="This quantity cannot be transferred ", readonly=True)
    accept_id = fields.Many2one('stock.picking')

    def action_accept(self):
        self.accept_id.button_validate(click=True)

    def action_reject(self):
        return True
