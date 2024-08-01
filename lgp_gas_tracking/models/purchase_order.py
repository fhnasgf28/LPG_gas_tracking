from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_lpg = fields.Boolean(string='Is Booking', default=False)