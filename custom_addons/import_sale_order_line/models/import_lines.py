# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount = fields.Float(string="Amount")
    # invoice_id = fields.Many2one('account.move')

    def action_import_lines(self):
        return {
            'name': "Import Lines Wizard",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.lines.wizard',
            'target': 'new',
            'context': {
                'invoice_line_ids': self.id
            }
        }

    def action_update_amount(self):
        if self.order_line:
            for amt in self.order_line:
                if amt.price_unit > 50:
                    amt.price_unit = self.amount

    # def action_register_payment_sale(self):
        # payment = self.env['account.payment'].create({
        #     'payment_type': 'inbound',
        #     'partner_type': 'customer',
        #     'amount': self.amount_total,
        #     'date': self.date_order,
        #     'currency_id': self.currency_id.id,
        #     'partner_id': self.partner_id.id,
        #     'ref': self.invoice_ids.name,
        #     'move_type': 'out_invoice'
        # })
        # return {
        #     'name': 'Register Payment',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'account.payment.register',
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'target': 'new',
        #     'context': {
        #         # 'active_model': 'account.move',
        #         'active_ids': self.ids,
        #     }
        # }
    def action_register_payment_sale(self):
        payment = self.env['account.move'].create({
            # 'payment_type': 'inbound',
            # 'amount': self.amount_total,
            'invoice_date': self.date_order,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids':
                [(0, 0, {
                    'name': self.order_line.name,
                    'quantity': self.order_line.product_uom_qty,
                    'price_unit': self.order_line.price_unit
                })
                 ],
        })
        # invoice_object = self
        # # cliente = self.env['res.partner'].search([('id', '=', self.partner_id.id)])
        # ctx = dict(
        #     active_ids=invoice_object.ids,  # Use ids and not id (it has to be a list)
        #     active_model='account.move',
        # )
        # values = {
        #     'payment_type': 'inbound',
        #     'partner_type': 'customer',
        #     'partner_id': self.partner_id.id,
        #     'payment_method_id': 1,
        #     'amount': self.amount_total,
        #     'payment_date': self.date_order,
        #     'currency_id': 1,
        #     'journal_id': 1,
        #     'communication': self.name,
        # }
        # wizard = self.env['account.payment.register'].with_context(ctx).create(values)
        # wizard._create_payments()



