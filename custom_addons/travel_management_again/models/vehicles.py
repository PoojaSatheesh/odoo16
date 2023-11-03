# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class TravelVehicles(models.Model):
    _name = "travel.vehicle"
    _description = "Travel Vehicle"
    _rec_name = "vehicle_name"

    reg_no = fields.Char("Registration Number")
    vehicle_type = fields.Selection(selection=[('bus', 'Bus'),
                                               ('traveller', 'Traveller'),
                                               ('van', 'Van'),
                                               ('others', 'Others')])
    vehicle_name = fields.Char()
    number_of_seats = fields.Integer(default=1)
    facilities_ids = fields.Many2many('vehicle.facilities')
    child_id = fields.One2many('vehicle.charges', 'parent_id')

    _sql_constraints = [
        ('field_unique',
         'unique(reg_no)',
         'Enter Correct Register number - it has to be unique!')
    ]

    @api.onchange('reg_no', 'vehicle_type')
    def onchange_(self, reg_no, vehicle_type, context=None):
        v = {}
        if reg_no and vehicle_type:
            v['name'] = reg_no + vehicle_type
        return {'value': v}


class VehicleFacilities(models.Model):
    _name = "vehicle.facilities"
    _description = "Vehicle Facilities"
    _rec_name = "facility"

    facility = fields.Char()


class VehicleCharges(models.Model):
    _name = "vehicle.charges"
    _description = "Vehicle Charges"

    service = fields.Char()
    quantity = fields.Integer(default=1)
    unit = fields.Char()
    amount = fields.Float()
    parent_id = fields.Many2one('travel.vehicle')
