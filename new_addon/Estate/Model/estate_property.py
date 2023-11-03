from datetime import timedelta

from dateutil import relativedelta

from odoo import fields, models, api


class Real_estate(models.Model):
    _name = "real.estate"
    _description = "Real Estate"

    name = fields.Char('Estate Name', required=True)
    description = fields.Text('Description', )
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Datetime.now() + timedelta(days=3*30), copy=False)
    expected_price = fields.Float(required=True, )
    selling_price = fields.Float(readonly=True)
    bedroom = fields.Integer(required=True, default=2)
    living_area = fields.Integer('Living Area (sqm)', required=True, )
    facades = fields.Integer(required=True, )
    garage = fields.Boolean(required=True, )
    gardens = fields.Boolean(required=True, )
    garden_area = fields.Integer('Garden Area (sqm)', required=True, )
    garden_orientation = fields.Selection(string='Type',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    active = fields.Boolean(required=True)
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer received', 'Offer Received'),
                                                         ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                         ('cancelled', 'Cancelled')], default='new')
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    property_tags = fields.Many2many("estate.property.tags", string="Property Tag")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    price = fields.One2many("estate.property.offer", "property_id", string="Price")
    # status = fields.One2many("estate.property.offer", "property_id", string="Status")
    best_offer = fields.Char(compute='_compute_best_offer')
    total_area = fields.Float(readonly=True, compute='_compute_area')

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('price', 'price')
    def _compute_best_offer(self):
        for offer in self:
            if offer.price:
                offer.best_offer = max(offer.price.mapped("price"))
            else:
                offer.best_offer = 0


class Property_types(models.Model):
    _name = "estate.property.type"
    _description = "Property types"

    name = fields.Char(required=True)


class Property_tags(models.Model):
    _name = "estate.property.tags"
    _description = "Property tags"

    name = fields.Char(required=True)


class Offers(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(string='Status',
                              selection=[('accepted', 'Accepted'), ('rejected', 'Rejected')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real.estate")
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute='_compute_deadline', inverse='_compute_validity')

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for dline in self:
            if dline.create_date:
                dline.deadline = dline.create_date + timedelta(days=dline.validity)

    def _compute_validity(self):
        for valid in self:
            if valid.create_date and valid.deadline:
                valid.validity = (valid.deadline - valid.create_date.date()).days


