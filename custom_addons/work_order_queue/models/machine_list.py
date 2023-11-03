# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class MachineList(models.Model):
    _name = "machine.list"
    _description = "Machine List"
    # _rec_name = "machines"

    name = fields.Char(string="Machines")