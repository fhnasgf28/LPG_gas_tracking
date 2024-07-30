# -*- coding: utf-8 -*-
import random
import string
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class LpgProduct(models.Model):
    _inherit = 'product.template'

    employee_id = fields.Many2one('hr.employee', string='Staff')
    name = fields.Char(string='Cylinder Name', required=True)
    is_full = fields.Boolean(string='Is Full', default=False)
    refill_date = fields.Datetime('Refill Date')
    return_date = fields.Datetime('Return Date')
    last_refill_date = fields.Date(string='Last Refill Date')
    customer_id = fields.Many2one('res.partner', string='Customer')
    arrival_date = fields.Date(string='Arrival Date')
    nama_toko = fields.Char(related="customer_id.nama_toko", string='Nama Toko')
    product_config_id = fields.Many2one('gas.lpg.config', string='Product Config Id')
    # stock_available = fields.Selection(related='product_config_id.status', string='Stock Available')


    @api.model
    def create(self, vals):
        if 'refill_date' not in vals:
            vals['refill_date'] = datetime.now() + timedelta(days=30)
        if 'return_date' not in vals:
            vals['return_date'] = datetime.now() + timedelta(days=30)
        if 'default_code' not in vals or not vals['default_code']:
            vals['default_code'] = self.generate_unique_code()
        product = super(LpgProduct, self).create(vals)
        product.product_variant_ids.write({'default_code': product.default_code})
        return product

    @api.constrains('refill_date', 'return_date')
    def _check_date(self):
        for record in self:
            if record.refill_date and record.return_date and record.refill_date >= record.return_date:
                raise ValidationError("Refill date must be earlier than return date.")

    @api.model
    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.digits, k=8))
            if not self.env['product.product'].search([('default_code', '=', code)]):
                return code

    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)', 'The default code must be unique for each product!')
    ]