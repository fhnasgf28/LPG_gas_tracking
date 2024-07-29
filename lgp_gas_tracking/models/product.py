# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LpgProduct(models.Model):
    _inherit = 'product.template'

    employee_id = fields.Many2one('hr.employee', string='Staff')
    name = fields.Char(string='Cylinder Name', required=True)
    is_full = fields.Boolean(string='Is Full', default=False)
    last_refill_date = fields.Date(string='Last Refill Date')
    customer_id = fields.Many2one('res.partner', string='Customer')
    arrival_date = fields.Date(string='Arrival Date')
    nama_toko = fields.Char(related="customer_id.nama_toko", string='Nama Toko')
    product_config_id = fields.Many2one('gas.lpg.config', string='Product Config Id')
    # stock_available = fields.Selection(related='product_config_id.status', string='Stock Available')

