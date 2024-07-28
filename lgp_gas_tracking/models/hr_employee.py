from odoo import models, fields, api, _


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    # lpg_shipment_ids = fields.One2many('lpg.tracking', 'employee_id', string='LPG Shipments')
    no_ktp = fields.Char(string='No. KTP')
    npwp = fields.Char(string='NPWP')
