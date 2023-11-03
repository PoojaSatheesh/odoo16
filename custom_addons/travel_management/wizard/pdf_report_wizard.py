# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date
from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from odoo.tools.safe_eval import json
import io
import xlsxwriter


class PdfReportWizard(models.TransientModel):
    _name = 'pdf.report.wizard'
    _description = "PDF Report Wizard"

    date_from = fields.Date(string="Date From",
                            help="Tour packages with booking date greater than or equal to the given date")
    date_to = fields.Date(string="Date To",
                          help="Tour packages with booking date less than or equal to the given date")
    partner_id = fields.Many2one(string="Customer", comodel_name="res.partner")
    vehicle_name = fields.Many2one(string="Vehicle Name", comodel_name="travels.vehicle")

    def query(self):

        date_from = self.date_from
        date_to = self.date_to
        partner_id = self.partner_id.id
        # partner_name = self.partner_id.name
        vehicle_name = self.vehicle_name.vehicle_name

        query = """
                    SELECT
                        travels_location.name AS source_loc_id,
                        tl.name AS destination_loc_id,
                        state,
                        tv.vehicle_name AS vehicle_list_id,
                        start_date,
                        end_date,
                        rp.name AS customer_id,
                        vce.subtotal as subtotal,
                        quotation_date
                    FROM
                        travels_tour_package AS ttp
                    INNER JOIN
                        travels_location
                    ON
                        ttp.source_loc_id = travels_location.id
                    INNER JOIN
                        travels_location AS tl
                    ON
                        ttp.destination_loc_id = tl.id
                    INNER JOIN
                        travels_vehicle AS tv
                    ON
                        ttp.vehicle_list_id = tv.id
                    INNER JOIN
                        res_partner AS rp
                    ON
                        ttp.customer_id = rp.id
                    INNER JOIN
                        vehicle_charge_estimation AS vce
                    ON
                        ttp.id = vce.tour_vehicle_parent_id
                    """

        tours = []
        if partner_id:
            query += """ and ttp.customer_id = %s"""
            tours.append(partner_id)

        if date_from:
            query += """and ttp.quotation_date >= %s """
            tours.append(date_from)

        if date_to:
            query += """and ttp.quotation_date <= %s """
            tours.append(date_to)

        if vehicle_name:
            query += """and tv.vehicle_name = %s """
            tours.append(vehicle_name)

        self.env.cr.execute(query, tuple(tours))
        report = self.env.cr.dictfetchall()
        print(report, "mmmmmmmm")
        if not report:
            raise ValidationError("No Record with that filter...No report printed")
        return report

    def print_pdf_report(self):

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_id': self.partner_id.id,
            'partner_name': self.partner_id.name,
            'vehicle_name': self.vehicle_name.vehicle_name,
        }
        print(data, ".....pp.")
        return self.env.ref('travel_management.action_tour_package_report_pdf').report_action(None, data=data)

    def print_xlsx_report(self):
        report = self.query()
        data = {
            'report': report,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_id': self.partner_id.id,
            'partner_name': self.partner_id.name,
            'vehicle_name': self.vehicle_name.vehicle_name,
        }
        print('data', data)

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'pdf.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Travel Management Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        partner_name = data.get('partner_name')
        vehicle_name = data.get('vehicle_name')
        user_obj = self.env.user
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        date_style = workbook.add_format(
            {'num_format': 'dd-mm-yyyy', 'align': 'center'})
        company_format = workbook.add_format(
            {'font_size': '12px'})
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format(
            {'font_size': '10px', 'align': 'center'})
        heading = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px'})

        sheet.set_column(1, 1, 40)
        sheet.set_column(2, 2, 25)
        sheet.set_column(2, 3, 30)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)
        sheet.set_column(8, 8, 20)
        sheet.set_column(9, 9, 20)

        sheet.merge_range('B7:F8', 'TRAVEL MANAGEMENT REPORT', head)
        sheet.write('B13', 'Print Date:', cell_format)
        sheet.write('C13', date.today(), date_style)

        sheet.write('B1', user_obj.company_id.name, company_format)
        sheet.write('B2', user_obj.company_id.street, company_format)
        sheet.write('B3', user_obj.company_id.city, company_format)
        sheet.write('B4', user_obj.company_id.zip, company_format)
        sheet.write('B5', user_obj.company_id.state_id.name, company_format)
        sheet.write('B6', user_obj.company_id.country_id.name, company_format)

        if date_from:
            sheet.write('B11', 'From Date:', cell_format)
            sheet.write('C11', date_from, txt)
        if date_to:
            sheet.write('D11', 'To Date:', cell_format)
            sheet.write('E11', date_to, txt)
        if partner_name:
            sheet.write('B12', 'Customer:', cell_format)
            sheet.write('C12', partner_name, txt)
        if vehicle_name:
            sheet.write('D12', 'Vehicle Name:', cell_format)
            sheet.write('E12', vehicle_name, txt)

        row = 16
        column = 0
        sl_no = 1
        if partner_name and vehicle_name:
            sheet.write('A15', 'SI.No', heading)
            sheet.write('B15', 'Source Location', heading)
            sheet.write('C15', 'Destination Location', heading)
            sheet.write('D15', 'Booking Date', heading)
            sheet.write('E15', 'Start Date', heading)
            sheet.write('F15', 'End Date', heading)
            sheet.write('G15', 'State', heading)
            sheet.write('H15', 'Total Amount', heading)
        elif partner_name:
            sheet.write('A15', 'SI.No', heading)
            sheet.write('B15', 'Source Location', heading)
            sheet.write('C15', 'Destination Location', heading)
            sheet.write('D15', 'Booking Date', heading)
            sheet.write('E15', 'Start Date', heading)
            sheet.write('F15', 'End Date', heading)
            sheet.write('G15', 'Vehicle Name', heading)
            sheet.write('H15', 'State', heading)
            sheet.write('I15', 'Total Amount', heading)
        elif vehicle_name:
            sheet.write('A15', 'SI.No', heading)
            sheet.write('B15', 'Customer', heading)
            sheet.write('C15', 'Source Location', heading)
            sheet.write('D15', 'Destination Location', heading)
            sheet.write('E15', 'Booking Date', heading)
            sheet.write('F15', 'Start Date', heading)
            sheet.write('G15', 'End Date', heading)
            sheet.write('H15', 'State', heading)
            sheet.write('I15', 'Total Amount', heading)
        else:
            sheet.write('A15', 'SI.No', heading)
            sheet.write('B15', 'Customer', heading)
            sheet.write('C15', 'Source Location', heading)
            sheet.write('D15', 'Destination Location', heading)
            sheet.write('E15', 'Booking Date', heading)
            sheet.write('F15', 'Start Date', heading)
            sheet.write('G15', 'End Date', heading)
            sheet.write('H15', 'Vehicle Name', heading)
            sheet.write('I15', 'State', heading)
            sheet.write('J15', 'Total Amount', heading)

        for rec in data['report']:
            if partner_name and vehicle_name:
                sheet.write(row, column, sl_no, txt)
                sheet.write(row, column + 1, rec.get('source_loc_id'), txt)
                sheet.write(row, column + 2, rec.get('destination_loc_id'), txt)
                sheet.write(row, column + 3, rec.get('quotation_date'), txt)
                sheet.write(row, column + 4, rec.get('start_date'), txt)
                sheet.write(row, column + 5, rec.get('end_date'), txt)
                sheet.write(row, column + 6, rec.get('state'), txt)
                sheet.write(row, column + 7, rec.get('subtotal'), txt)
            elif partner_name:
                sheet.write(row, column, sl_no, txt)
                sheet.write(row, column+1, rec.get('source_loc_id'), txt)
                sheet.write(row, column+2, rec.get('destination_loc_id'), txt)
                sheet.write(row, column+3, rec.get('quotation_date'), txt)
                sheet.write(row, column+4, rec.get('start_date'), txt)
                sheet.write(row, column+5, rec.get('end_date'), txt)
                sheet.write(row, column+6, rec.get('vehicle_list_id'), txt)
                sheet.write(row, column+7, rec.get('state'), txt)
                sheet.write(row, column+8, rec.get('subtotal'), txt)
            elif vehicle_name:
                sheet.write(row, column, sl_no, txt)
                sheet.write(row, column + 1, rec.get('customer_id'), txt)
                sheet.write(row, column + 2, rec.get('source_loc_id'), txt)
                sheet.write(row, column + 3, rec.get('destination_loc_id'), txt)
                sheet.write(row, column + 4, rec.get('quotation_date'), txt)
                sheet.write(row, column + 5, rec.get('start_date'), txt)
                sheet.write(row, column + 6, rec.get('end_date'), txt)
                sheet.write(row, column + 7, rec.get('state'), txt)
                sheet.write(row, column + 8, rec.get('subtotal'), txt)
            else:
                sheet.write(row, column, sl_no, txt)
                sheet.write(row, column + 1, rec.get('customer_id'), txt)
                sheet.write(row, column + 2, rec.get('source_loc_id'), txt)
                sheet.write(row, column + 3, rec.get('destination_loc_id'), txt)
                sheet.write(row, column + 4, rec.get('quotation_date'), txt)
                sheet.write(row, column + 5, rec.get('start_date'), txt)
                sheet.write(row, column + 6, rec.get('end_date'), txt)
                sheet.write(row, column + 7, rec.get('vehicle_list_id'), txt)
                sheet.write(row, column + 8, rec.get('state'), txt)
                sheet.write(row, column + 9, rec.get('subtotal'), txt)

            row += 1
            column = 0
            sl_no += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
