# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TourPackage(models.Model):
    _name = "travels.tour.package"
    _description = "Tour Package"
    _rec_name = "customer_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    quotation_date = fields.Date(default=fields.Date.today(), string="Date", help="Quotation Date")
    source_loc_id = fields.Many2one("travels.location", string='Source Location', required=True,
                                    domain="[('id', '!=', destination_loc_id)]")
    destination_loc_id = fields.Many2one("travels.location", string='Destination Location', required=True,
                                         domain="[('id', '!=', source_loc_id)]",
                                         help="Location where you are planning to go")
    start_date = fields.Date(required=True, string="Start Date", help="Tour start date")
    end_date = fields.Date(required=True, string="End Date", help="Tour end date")
    no_travellers = fields.Integer(required=True, string="Number of Travellers", default=1)
    facilities_ids = fields.Many2many('travels.vehicle.facilities', string='Facilities')
    vehicle_type = fields.Selection(selection=[
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('others', 'Others')
    ], string="Vehicle Type")
    available_vehicles_ids = fields.Many2many('travels.vehicle', compute='_compute_vehicle_list')
    vehicle_list_id = fields.Many2one('travels.vehicle', domain="[('id', 'in', available_vehicles_ids)]")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, default='draft')
    estimated_km = fields.Float(string="Estimated km")
    package_charge_ids = fields.One2many('vehicle.charge.estimation', "tour_vehicle_parent_id")
    company_id = fields.Many2one("res.company", readonly=True,
                                 default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users')

    @api.constrains('start_date', 'end_date')
    def date_constraints(self):
        """function to get error message if end date less than start date"""
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError('Sorry, End date  must be after Start Date...')
            elif rec.quotation_date > rec.start_date:
                raise ValidationError('Sorry, Start date Cannot be less than Quotation Date')

    def action_confirmed(self):
        """button confirm"""
        self.write({
            'state': "confirmed"
        })
        """automatically create booking when confirming a tour package"""
        data = self.env['travel.management'].create({
            'customer_id': self.customer_id.id,
            'source_location_id': self.source_loc_id.id,
            'destination_location_id': self.destination_loc_id.id,
            'travel_date': self.start_date,
            'company_id': self.company_id.id,
        })
        for record in self.package_charge_ids:
            data.package_child_ids = [
                (0, 0, {
                    'service_id': record.service_id.id,
                })
            ]

        """when confirming check if the vehicle chosen is booked and show warning message"""
        existing_bookings = self.env['travels.tour.package'].search([
            ('id', '!=', self.ids),
            ('state', '=', 'confirmed'),
            ('vehicle_list_id', '!=', False),
            ('start_date', '<=', self.end_date),
            ('end_date', '>=', self.start_date),
        ])

        vehicles_in_use = existing_bookings.mapped('vehicle_list_id.id')
        print(self.vehicle_list_id)
        if self.vehicle_list_id.id in vehicles_in_use:
            raise ValidationError("This vehicle has been booked by Someone else ... Please choose another vehicle")
        else:
            print("111111111111111111111")

    @api.depends('start_date', 'end_date', 'no_travellers', 'facilities_ids', 'vehicle_type')
    def _compute_vehicle_list(self):
        """vehicle list based on vehicle type, number of travellers, start date, end date and facilities"""

        domain = []
        available_vehicles = []
        for rec in self:
            if rec.vehicle_type:
                domain.append(('vehicle_type', '=', self.vehicle_type))
            if rec.no_travellers:
                domain.append(('num_of_seats', '>=', self.no_travellers))
            if rec.start_date and rec.end_date:
                current_booking_start_date = rec.start_date
                current_booking_end_date = rec.end_date

                existing_bookings = self.env['travels.tour.package'].search([
                    ('state', '=', 'confirmed'),
                    ('vehicle_list_id', '!=', False),
                    ('start_date', '<=', current_booking_end_date),
                    ('end_date', '>=', current_booking_start_date),
                ])
                print(existing_bookings)
                vehicles_in_use = existing_bookings.mapped('vehicle_list_id.id')
                domain.append(('id', 'not in', vehicles_in_use))

            rec.available_vehicles_ids = self.env['travels.vehicle'].search(domain)
            if rec.facilities_ids:
                for vehicle in self.env['travels.vehicle'].search(domain):
                    if len(rec.facilities_ids) == 1:
                        for item in rec.facilities_ids.ids:
                            if item in vehicle.facilities_ids.ids:
                                available_vehicles.append(vehicle.id)
                    elif len(rec.facilities_ids) > 1:
                        if len(rec.facilities_ids.ids) == len(vehicle.facilities_ids.ids):
                            facility_sorted = sorted(rec.facilities_ids.ids)
                            print("11:", rec.facilities_ids.ids, "facility_sorted", facility_sorted)
                            facility_in_vehicle_sorted = sorted(vehicle.facilities_ids.ids)
                            if facility_sorted == facility_in_vehicle_sorted:
                                available_vehicles.append(vehicle.id)
                        else:
                            if set(rec.facilities_ids.ids).issubset(set(vehicle.facilities_ids.ids)):
                                available_vehicles.append(vehicle.id)
            rec.available_vehicles_ids = available_vehicles


class Estimation(models.Model):
    _name = "vehicle.charge.estimation"
    _description = "Estimation"

    service_id = fields.Many2one('vehicle.charges', string='Service', help="Service provided by vehicle")
    quantity = fields.Integer(default=1, related='service_id.quantity', readonly=False, string="Quantity")
    amount = fields.Float(related='service_id.amount', readonly=False)
    subtotal = fields.Float(string="SubTotal", compute='_compute_subtotal', store=True)
    tour_vehicle_parent_id = fields.Many2one("travels.tour.package")
    package_parent_id = fields.Many2one("travel.management")

    @api.depends('quantity', 'amount')
    def _compute_subtotal(self):
        """calculate subtotal
        subtotal = quantity * amount """
        for record in self:
            if record.quantity and record.amount:
                record.subtotal = record.quantity * record.amount
            else:
                record.subtotal = None
