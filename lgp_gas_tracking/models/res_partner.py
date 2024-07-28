from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    no_ktp = fields.Char(string='No. KTP')
    npwp = fields.Char(string='NPWP')
    nama_toko = fields.Char(string='Nama Toko')
