# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta, date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TravelManagement(models.Model):
    """to get travel management option"""
    _name = "travel.management"
    _description = "Travel Management"
    _order = 'travel_date'
    _rec_name = 'booking_reference'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    booking_reference = fields.Char(readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    passengers = fields.Integer(string="No of Passengers", default=1, help="Number of Passengers")
    services = fields.Selection(string='Service', help="Service Vehicle",
                                selection=[('flight', 'Flight'), ('train', 'Train'), ('bus', 'Bus')])
    booking_date = fields.Datetime(default=fields.Date.today(), required=True, string="Booking Date")
    source_location_id = fields.Many2one("travels.location", string='Source Location', required=True,
                                         help="Source Location",
                                         domain="[('id', '!=', destination_location_id)]")
    destination_location_id = fields.Many2one("travels.location", string='Destination Location', required=True,
                                              tracking=True, help="Destination Location",
                                              domain="[('id', '!=', source_location_id)]")
    travel_date = fields.Datetime(string='Travelling Date', required=True, help="Date when you are travelling")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('expired', 'Expired'),
        ('paid', 'Paid'),
    ], string='Status', readonly=True, copy=False,
        tracking=True, default='draft')
    service_types_id = fields.Many2one("travels.service.types", string="Package Service",
                                       help="Package services which can calculate expiration date")
    expiration_date = fields.Date(compute='_compute_expiration_date', store=True, string="Expiration Date")
    package_child_ids = fields.One2many('vehicle.charge.estimation', 'package_parent_id')
    fees = fields.Float(string='Fees/Charges')
    invoice_id = fields.Many2one('account.move')
    invoice = fields.Boolean()
    paid_state = fields.Boolean(compute='_compute_payment_state', store=True)
    company_id = fields.Many2one("res.company", readonly=True,
                                 default=lambda self: self.env.company, string="Company")
    user_id = fields.Many2one('res.users')

    # reference = fields.Reference

    def action_confirm(self):
        """button for confirming travel booking"""
        self.write({'state': "confirmed"})
        if self.fees and not self.expiration_date:
            self.write({'state': "confirmed"})
        elif self.expiration_date < date.today():
            self.write({'state': "expired"})

    def action_create_invoice(self):
        """function to create invoice"""
        self.invoice = True
        for rec in self:
            description = rec.booking_reference + ' ' + str(rec.services)
            payment = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.customer_id.id,
                'invoice_date': self.booking_date,
                'date': self.travel_date,
            })
            if self.service_types_id:
                for record in self.package_child_ids:
                    payment.invoice_line_ids = [
                        (0, 0, {
                            'name': record.service.service_id,
                            'quantity': record.quantity,
                            'price_unit': record.amount,
                        })
                    ]
            else:
                payment.invoice_line_ids = [
                    (0, 0, {
                        'name': description,
                        'price_unit': self.fees,
                    })
                ]
            self.invoice_id = payment

            return {
                'type': 'ir.actions.act_window',
                'name': 'Booking Invoice',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': payment.id,
                'target': 'current',
            }

    def invoice_tab(self):
        """ smart tab for invoice"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }

    @api.depends('invoice_id.payment_state')
    def _compute_payment_state(self):
        """change state to paid"""
        for record in self:
            if record.invoice_id.payment_state == 'paid':
                record.write({'state': 'paid', 'paid_state': True})

    @api.constrains('travel_date', 'booking_date')
    def date_constrains(self):
        """function to show error message if travelling date is before booking date"""
        for rec in self:
            if rec.travel_date < rec.booking_date:
                raise ValidationError('Sorry, Travelling date  must be after Booking Date...')

    @api.model
    def create(self, vals):
        """function to set sequence for booking reference"""
        if vals.get('booking_reference', _('New')) == _('New'):
            vals['booking_reference'] = self.env['ir.sequence'].next_by_code(
                'booking_reference')
        return super(TravelManagement, self).create(vals)

    @api.depends('booking_date', 'service_types_id')
    def _compute_expiration_date(self):
        """function to calculate expiration date depending on booking date and service type"""
        for expiry in self:
            if expiry.service_types_id:
                expiry.expiration_date = expiry.booking_date + timedelta(
                    days=expiry.service_types_id.expiration
                )
            else:
                expiry.expiration_date = None


class Locations(models.Model):
    """to create and edit locations"""
    _name = "travels.location"
    _description = "Locations"

    name = fields.Char('Location Name')
    company_id = fields.Many2one("res.company", readonly=True, string="Company",
                                 default=lambda self: self.env.company)


class ServiceTypes(models.Model):
    """To add and edit a service type and add expiration date for booking"""
    _name = "travels.service.types"
    _description = "Service Types"

    name = fields.Char(string="Service Name")
    expiration = fields.Integer("Expiration", help="No of days to expire")
    company_id = fields.Many2one("res.company", readonly=True, string="Company",
                                 default=lambda self: self.env.company)
