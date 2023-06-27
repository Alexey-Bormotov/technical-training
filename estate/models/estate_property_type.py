from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    name = fields.Char('Property type', required=True)
    sequence = fields.Integer(
        'Sequence',
        default=1,
        help='Used to order property types. Lower is higher.'
    )
    offer_count = fields.Integer(
        'Offer count',
        compute='_compute_offer_count'
    )

    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The type name must be unique.')
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
