# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class Vehicle(models.Model):
    _name = "travels.vehicle"
    _description = "Vehicle"
    _rec_name = 'reg_no'

    reg_no = fields.Char('Registration NO')
    vehicle_type = fields.Selection(selection=[
        ('bus', 'Bus'),
        ('traveller', 'Traveller'),
        ('van', 'Van'),
        ('others', 'Others')
    ])
    vehicle_name = fields.Char('Vehicle Name')
    num_of_seats = fields.Integer('Number of Seats', default=1)
    facilities_ids = fields.Many2many('travels.vehicle.facilities', string="Facilities",)
    vehicle_charge_ids = fields.One2many('vehicle.charges', "vehicle_charge_parent_id")
    company_id = fields.Many2one("res.company", readonly=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('field_unique',
         'unique(reg_no)',
         'Type Correct Registration Number - it has to be unique!')
    ]

    @api.onchange('reg_no', 'vehicle_type')
    def _onchange_reg_no_vehicle_type(self):
        """vehicle name = reg no + vehicle type"""
        if self.reg_no and self.vehicle_type:
            self.vehicle_name = f"{self.reg_no} {self.vehicle_type}"
        else:
            self.vehicle_name = False


class VehicleCharges(models.Model):
    _name = "vehicle.charges"
    _description = "Vehicle Charges"
    _rec_name = 'service'

    service = fields.Char('Service')
    quantity = fields.Integer(default=1, string="Quantity")
    unit_id = fields.Many2one(comodel_name='uom.uom', string="Unit")
    amount = fields.Float('Amount')
    vehicle_charge_parent_id = fields.Many2one("travels.vehicle")


class VehicleFacilities(models.Model):
    _name = "travels.vehicle.facilities"
    _description = "Vehicle Facilities"
    _rec_name = 'facilities'

    facilities = fields.Char('Vehicle Facilities')
    company_id = fields.Many2one("res.company", readonly=True,
                                 default=lambda self: self.env.company, string="Company")

