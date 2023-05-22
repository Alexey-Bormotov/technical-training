from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char('Property type', required=True)
