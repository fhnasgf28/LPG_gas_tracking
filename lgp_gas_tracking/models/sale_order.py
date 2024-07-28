from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'sale order lpg gas refil'

    is_lpg = fields.Boolean(string='Is LPG Product', default=False)
    lpg_quantity = fields.Float(string='LPG Quantity (kg)', default=0.0)
    lpg_type = fields.Selection([
        ('lpg3', 'Gas LPG 3 Kg'),
        ('lpg12', 'Gas LPG 12 Kg'),
    ], string='LPG Type')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Delivery Vehicle')
    driver_name = fields.Char(string="Driver Name", related="vehicle_id.driver_id.name", readonly=True)
    gas_tracking_ids = fields.One2many('gas.tracking', 'sale_order_id', string='Gas Tracking Records')
    product_id = fields.Many2one('product.template', string='Gas Product')
    nama_toko= fields.Char(related="partner_id.nama_toko", string='Nama Toko')


    @api.model
    def create(self, vals):
        if vals.get('is_lpg'):
            sequence_code = 'gas.order'
        else:
            sequence_code = 'sale.order'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or _('New')
        res = super(SaleOrder, self).create(vals)
        return res
