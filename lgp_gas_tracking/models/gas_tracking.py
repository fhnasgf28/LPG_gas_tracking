from odoo import models, fields, api


class GasTracking(models.Model):
    _name = 'gas.tracking'
    _description = 'Gas Tracking'

    name = fields.Char(string='Tracking Number', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('gas.tracking'))
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    product_id = fields.Many2one('product.template', string='Gas Product', related='sale_order_id.product_id')
    status = fields.Selection([
        ('available', 'Available'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ], string='Status', default='available')
    location_id = fields.Many2one('stock.location', string='Current Location')
    delivery_date = fields.Datetime(string='Delivery Date')
    return_date = fields.Datetime(string='Return Date')
