from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char('Property tag', required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The tag name must be unique.')
    ]
