# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, api, fields
from odoo.exceptions import ValidationError, UserError


class TourPackage(models.Model):
    _name = "travels.tour.packages"
    _description = "travels and tour packages"
    _rec_name = "customer_id"

    customer_id = fields.Many2one('res.partner', string='Customer',
                                  required=True)
    quotation_date = fields.Date(string="Quotation Date",
                                 default=fields.Date.today, readonly=True)
    src_location_id = fields.Many2one('travels.locations',
                                      string="Source location",
                                      required=True)
    dst_location_id = fields.Many2one('travels.locations',
                                      string="Destination location",
                                      required=True)
    start_date = fields.Date(string="Start date", default=fields.Date.today(),
                             required=True)
    end_date = fields.Date(string="End date", default=fields.Date.today(),
                           required=True)
    no_of_travellers = fields.Integer(string="Number of travellers", default=1)
    facilities_ids = fields.Many2many('travels.vehicle.facilities',
                                      string="Facilities")
    vehicle_type = fields.Selection(
        [('bus', 'Bus'), ('traveller', 'Traveller'), ('van', 'Van'),
         ('other', 'Other')],
        string='Vehicle Type')
    vehicle_id = fields.Many2one("travels.vehicle", string="Vehicle List",
                                 required=True)
    estimated_km = fields.Integer(string="Estimated KM")
    vehicle_estimation_ids = fields.One2many('travels.package.estimation',
                                             'packages_id')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')],
                             default='draft',
                             string="State")
    booking_reference = fields.Char(string='Booking Reference')

    @api.onchange('src_location_id')
    def _onchange_src_location_id(self):
        """For location hide in destination location"""

        if self.src_location_id:
            return {'domain': {'dst_location_id': [
                ('location', '!=', self.src_location_id.location)]}}
