# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    tolerance = fields.Integer('Tolerance',
                               help='Give the tolerance number')
