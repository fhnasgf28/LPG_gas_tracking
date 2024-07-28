from odoo import models, fields, api


class SaleOrderConfig(models.Model):
    _name = 'gas.lpg.config'
    _description = 'Sale Order Configuration'

    product_id = fields.Many2one('product.product', string='Product')
    available_stock = fields.Float(string='Available Stock')
    status = fields.Selection([
        ('unavailable', 'Unavailable'),
        ('available', 'Available')
    ], string='Status', default='unavailable', compute='_compute_status')

    @api.depends('product_id', 'available_stock')
    def _compute_status(self):
        for record in self:
            if record.product_id and record.available_stock > 0:
                record.status = 'available'
            else:
                record.status = 'unavailable'
