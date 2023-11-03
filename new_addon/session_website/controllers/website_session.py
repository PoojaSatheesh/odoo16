from odoo.http import Controller, request, route


class Partner(Controller):
    @route(route='/partner', auth='user', website=True)
    def partner(self):
        print('Hello ', request.env.uid)
        country_ids = request.env['res.country'].search([])
        return request.render('session_website.website_session',
                              {'country_ids': country_ids
                               })

    @route('/create/partner')
    def create_partner(self, name, email, **kw):
        print("create partner", name, email, kw)
        partner_id = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': kw.get('phone'),
            'street': kw.get('street'),
            'country_id': kw.get('country')
        })
        partner_ids = request.env['res.partner'].sudo().search([], limit=4, order='create_date')
        return request.render('session_website.website_session',
                              {'partner_id': partner_id, 'partner_ids': partner_ids})

    @route(['''/view/partner//<model("res.partner"):partner>'''], auth='public', website=True)
    def view_partner(self, partner):
        print('view', partner)
        return request.render('session_website.website_partner_view_template', {'partner': partner})
