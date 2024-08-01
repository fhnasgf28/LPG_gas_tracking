from odoo import models, fields, api, exceptions
from datetime import timedelta


class GasTransaction(models.Model):
    _name = 'gas.transaction'
    _description = 'Gas Transaction'

    product_id = fields.Many2one('product.product', string='Gas Product', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    transaction_date = fields.Date(string='Transaction Date', default=fields.Date.context_today)
    due_date = fields.Date(compute='_compute_due_date', string='Due Date', store=True)
    default_code = fields.Char(related='product_id.default_code', string='Serial Number', readonly=True)
    # last_refill_date = fields.Date(related='product_id.last_refill_date', string='Last_Refill Date', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Staff')
    transaction_state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('empty', 'Empty'),
        ('done', 'Done'),
    ], string='Transaction State', compute='_compute_transaction_state', store=True, default='available')
    profit = fields.Float(compute='_compute_profit', string='Profit', store=True)

    @api.depends('transaction_date')
    def _compute_due_date(self):
        pass

    @api.depends('product_id')
    def _compute_profit(self):
        for record in self:
            record.profit = record.product_id.list_price if record.transaction_state == 'done' else 0.0

    @api.model
    def create(self, vals):
        record = super(GasTransaction, self).create(vals)
        if record.product_id:
            record.product_id.write({'state': 'in_use'})
            record.write({'transaction_state': 'in_use'})
        return record

    @api.depends('transaction_date')
    def _compute_due_dat(self):
        for record in self:
            if record.transaction_state:
                transaction_date = fields.Date.from_string(record.transaction_state)
                due_date = transaction_date + timedelta(days=7)
                record.due_date = fields.Date.to_string(due_date)
            else:
                record.due_date = False