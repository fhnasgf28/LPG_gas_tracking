from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'sale order lpg gas refil'

    is_lpg = fields.Boolean(string='Is LPG Product', default=False)
    rfq_created = fields.Boolean(string="RFQ Created", default=False)
    lpg_quantity = fields.Float(string='LPG Quantity (kg)', default=0.0)
    lpg_type = fields.Selection([
        ('lpg3', 'Gas LPG 3 Kg'),
        ('lpg12', 'Gas LPG 12 Kg'),
    ], string='LPG Type')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Delivery Vehicle')
    driver_name = fields.Char(string="Driver Name", related="vehicle_id.driver_id.name", readonly=True)
    gas_tracking_ids = fields.One2many('gas.tracking', 'sale_order_id', string='Gas Tracking Records')
    product_id = fields.Many2one('product.template', string='Gas Product')
    nama_toko = fields.Char(related="partner_id.nama_toko", string='Nama Toko')
    refill_date = fields.Date(related='order_line.product_id.refill_date', string='Refill Date', readonly=True)
    return_date = fields.Date(related='order_line.product_id.return_date', string='Return Date', readonly=True)

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

    def action_create_rfq(self):
        for record in self:
            if record.rfq_created:
                raise ValidationError(f'Product {record.name} already been added to RFQ.')
            sequence_name = self.env['ir.sequence'].next_by_code('gas.request.quotation') or _('New')
            rfq = self.env['purchase.order'].create({
                'partner_id': record.partner_id.id,
                'date_order': fields.Datetime.now(),
                'name': sequence_name,
                'is_lpg': True,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'date_planned': fields.Datetime.now()
                }) for line in record.order_line]
            })
            record.rfq_created = True
            return {
                'name': 'RFQ Created',
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'res_id': rfq.id,
                'view_mode': 'form',
            }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_id', 'product_uom_qty')
    def _check_available_stock(self):
        for line in self:
            config = self.env['gas.lpg.config'].search([('product_id', '=', line.product_id.id)], limit=1)
            if config:
                if line.product_uom_qty > config.available_stock:
                    raise ValidationError(
                        f"The Quantity ordered for {line.product_id.name} exceeds the available stock of {config.available_stock}")

    @api.model
    def create(self, vals):
        record = super(SaleOrderLine, self).create(vals)
        self._update_available_stock(record.product_id.id, - record.product_uom_qty)
        return record

    def write(self, vals):
        for record in self:
            if "product_uom_qty" in vals:
                quantity_diff = vals["product_uom_qty"] - record.product_uom_qty
                self._update_available_stock(record.product_id.id, - quantity_diff)
        return super(SaleOrderLine, self).write(vals)

    def unlink(self):
        for record in self:
            self._update_available_stock(record.product_id.id, record.product_uom_qty)
        return super(SaleOrderLine, self).unlink()

    def _update_available_stock(self, product_id, quantity_change):
        config = self.env["gas.lpg.config"].search([('product_id', '=', product_id)], limit=1)
        if config:
            new_stock = config.available_stock + quantity_change
            if new_stock < 0:
                raise UserError(
                    f"Stock for {config.product_id.name} is insufficient. Available stock: {config.available_stock}.")
            config.sudo().write({'available_stock': new_stock})
