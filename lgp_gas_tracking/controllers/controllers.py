# -*- coding: utf-8 -*-
# from odoo import http


# class LgpGasTracking(http.Controller):
#     @http.route('/lgp_gas_tracking/lgp_gas_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lgp_gas_tracking/lgp_gas_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lgp_gas_tracking.listing', {
#             'root': '/lgp_gas_tracking/lgp_gas_tracking',
#             'objects': http.request.env['lgp_gas_tracking.lgp_gas_tracking'].search([]),
#         })

#     @http.route('/lgp_gas_tracking/lgp_gas_tracking/objects/<model("lgp_gas_tracking.lgp_gas_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lgp_gas_tracking.object', {
#             'object': obj
#         })
