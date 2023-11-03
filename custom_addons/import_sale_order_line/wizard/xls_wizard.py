# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import binascii
import xlrd

from odoo import models, fields
from odoo.exceptions import UserError


class ImportLineWizard(models.TransientModel):
    _name = 'import.lines.wizard'
    _description = 'Import Lines Wizard'

    import_file = fields.Binary(string='Import xls', help="Upload file")

    def import_order_lines(self):
        try:
            data = binascii.a2b_base64(self.import_file)
            book = xlrd.open_workbook(file_contents=data)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.import_file)
        except xlrd.biffh.XLRDError:
            raise UserError('Only Excel files are supported.')
        for sheet in book.sheets():
            try:
                line_vals = []
                if sheet.name == 'Sheet1':
                    for row in range(sheet.nrows):
                        if row > 0:
                            row_values = sheet.row_values(row)
                            vals = self._create_order_line(row_values)
                            line_vals.append((0, 0, vals))
            except IndexError:
                pass

    def _create_order_line(self, record):
        """function to create sale order line when an Excel sheet is imported and
        if the product in Excel sheet is not present in products it creates a new product with that name"""
        context = self.env.context

        product = self.env['product.product'].search([('name', '=', record[0])], limit=1)
        if record[0]:
            if not product:
                product = self.env['product.product'].create({
                    'name': record[0],
                })

            sale_order_line = self.env['sale.order.line'].create({
                'order_id': context['order_id'],
                'product_id': product.id,
                'product_uom_qty': record[1] or 1,
                'product_uom': product.uom_id.id,
                'name': record[3] or record[0],
                'price_unit': record[4]
            })
            return sale_order_line
