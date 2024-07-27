from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    sale_order_ids = fields.One2many('sale.order', 'vehicle_id', string='Sale Orders')
