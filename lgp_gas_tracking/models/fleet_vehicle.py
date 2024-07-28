from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    sale_order_ids = fields.One2many('sale.order', 'vehicle_id', string='Sale Orders')
    driver_ktp = fields.Char(related='driver_id.no_ktp', string='Driver No. KTP', readonly=True)
    driver_npwp = fields.Char(related='driver_id.npwp', string='Driver NPWP', readonly=True)
