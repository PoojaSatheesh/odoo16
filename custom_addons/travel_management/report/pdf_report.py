# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api
from odoo.exceptions import ValidationError


class PdfReport(models.AbstractModel):
    _name = "report.travel_management.tour_report"
    _description = "Tour Package PDF Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        print(data, "data.....")
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        partner_id = data.get('partner_id')
        vehicle_name = data.get('vehicle_name')

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
            query += """and ttp.quotation_date >= %s"""
            tours.append(date_from)

        if date_to:
            query += """and ttp.quotation_date <= %s"""
            tours.append(date_to)

        if vehicle_name:
            query += """and tv.vehicle_name = %s"""
            tours.append(vehicle_name)

        self.env.cr.execute(query, tours)
        report = self.env.cr.dictfetchall()
        print(report, "kkkkk")
        if not report:
            raise ValidationError("No Record with that filter...No report printed")

        return {
            'data': data,
            'report': report
        }
