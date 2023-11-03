# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.http import Controller, route, request


class TravelBooking(Controller):

    @route('/booking', auth="public", website=True)
    def travel_booking(self, **kw):
        customer_id = request.env['res.partner'].sudo().search([])
        source_location_id = request.env['travels.location'].sudo().search([])
        destination_location_id = request.env['travels.location'].sudo().search([])
        return request.render('travel_management.website_booking', {
            'customer_id': customer_id, 'source_location_id': source_location_id,
            'destination_location_id': destination_location_id
        })

    @route('/create/booking', auth="public", website=True)
    def create_booking(self, **kw):
        print(kw)
        name_id = kw.get('customer_id')
        name = int(name_id)
        source_loc_id = kw.get('source_location_id')
        source_loc = int(source_loc_id)
        destination_loc_id = kw.get('destination_location_id')
        destination_loc = int(destination_loc_id)
        request.env['travel.management'].sudo().create({
            'customer_id': name,
            'booking_date': kw.get('booking_date'),
            'passengers': kw.get('passengers'),
            'source_location_id': source_loc,
            'destination_location_id': destination_loc,
            'travel_date': kw.get('travel_date'),
        })
        return request.render("travel_management.booking_thanks", {})

    @route('/bookings', auth="public", website=True)
    def booking_list(self):
        bookings = request.env['travel.management'].sudo().search([])
        # print('bookings..........', bookings)
        return request.render('travel_management.bookings_list',
                              {'bookings': bookings})

