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
        help="Used to order property types. Lower is better."
    )

    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Properties"
    )

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The type name must be unique.')
    ]
