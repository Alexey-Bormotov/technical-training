from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char('Property tag', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The tag name must be unique.')
    ]
