from odoo import models, fields, api


class GasTracking(models.Model):
    _name = 'gas.tracking'
    _description = 'Gas Tracking'

    product_code = fields.Char(related='product_id.default_code', string='Tracking Number', copy=False, readonly=True, index=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    product_id = fields.Many2one('product.template', string='Gas Product')
    status = fields.Selection([
        ('available', 'Available'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ], string='Status', default='available')
    location_id = fields.Many2one('stock.location', string='Current Location')
    delivery_date = fields.Datetime(string='Delivery Date')
    return_date = fields.Datetime(string='Return Date')
