from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = One2many(
        'estate.property',
        'salesman_id',
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])]
    )