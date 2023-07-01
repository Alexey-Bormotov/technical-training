from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Users, upgraded to salesmen'

    property_ids = fields.One2many(
        'estate.property',
        'salesman_id',
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])]
    )
