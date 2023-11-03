# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.http import request, route, Controller


class BookingDetails(Controller):
    @route(['/booking_details'], type="json", auth="public", website=True, methods=['POST'])
    def all_bookings(self):
        booking_ids = request.env['travel.management'].search_read([])
        # print(".....", booking_ids)
        return booking_ids

    @route(['/booking_form/<id>'], auth="public", website=True)
    def booking_form(self, id):
        print('hyyyyyy')
        travel_booking = request.env['travel.management'].browse(int(id))
        print(travel_booking)
        return request.render('travel_management.bookings_form_view',
                              {'travel_booking': travel_booking})
