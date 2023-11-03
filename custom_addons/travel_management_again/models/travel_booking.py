# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta, date

from odoo import models, fields, _, api


class TravelBooking(models.Model):
    _name = "travel.booking"
    _description = "Travel Booking Again"
    _rec_name = "booking_reference"
    _order = 'traveling_date'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    booking_reference = fields.Char(readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Customer")
    number_of_passengers = fields.Integer(default=1)
    service_type = fields.Selection(string='Service Type',
                                    selection=[('flight', 'Flight'), ('train', 'Train'), ('bus', 'Bus')])
    booking_date = fields.Datetime(default=fields.Datetime.today(), required=True)
    source_location_id = fields.Many2one('travel.location', string="Source Location",
                                         domain="[('id', '!=', destination_location_id)]")
    destination_location_id = fields.Many2one('travel.location', "Destination Location",
                                              domain="[('id', '!=', ""source_location_id)]")
    traveling_date = fields.Datetime()
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('expired', 'Expired'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, default='draft')
    service_id = fields.Many2one('travel.service.type', string="Package")
    expiration_date = fields.Date(readonly=True, compute='_compute_expiration_date')

    def button_confirm(self):
        if self.expiration_date > date.today():
            self.write({'state': "confirmed"})
        else:
            self.write({'state': 'expired'})

    @api.model
    def create(self, vals):
        """Sequence number"""
        if vals.get('booking_reference', _('New')) == _('New'):
            vals['booking_reference'] = self.env['ir.sequence'].next_by_code(
                'travel.booking')
        return super(TravelBooking, self).create(vals)

    @api.constrains('booking_date', 'travelling_date')
    def _check_travelling_date(self):
        for record in self:
            if record.booking_date > record.traveling_date:
                raise ValueError("Sorry......Travelling date cannot be ")

    @api.depends('booking_date', 'service_id')
    def _compute_expiration_date(self):

        for record in self:
            if record.service_id:
                record.expiration_date = record.booking_date + timedelta(days=record.service_id.
                                                                         expiration_days)
            else:
                record.expiration_date = None
                print(record.expiration_date)


class TravelLocation(models.Model):
    _name = "travel.location"
    _description = "Locations"
    _rec_name = "location"

    location = fields.Char()


class ServiceType(models.Model):
    _name = "travel.service.type"
    _description = "Service Type"

    name = fields.Char(string="Service Type")
    expiration_days = fields.Integer()
