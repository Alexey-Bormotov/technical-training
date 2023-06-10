from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=lambda self: self._default_date_availability()
    )
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area (sq.m.)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area (sq. m.)')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    total_area = fields.Integer(
        'Total area',
        compute='_compute_total_area'
    )
    best_price = fields.Float(
        'Best price',
        compute='_compute_best_price'
    )

    property_type_id = fields.Many2one(
        'estate.property.type', string='Property type'
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )
    salesman_id = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Property tags'
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Property offers'
    )

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new'
    )

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped('price')
            ) if record.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else False

    def action_sold_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold.')
            record.state = 'sold'

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled.')
            record.state = 'cancelled'

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(
                    record.selling_price, precision_rounding=0.01
                )
                and float_compare(
                    record.selling_price, record.expected_price * 0.9,
                    precision_rounding=0.01
                ) < 0
            ):
                raise ValidationError(
                    'The selling price must be at least '
                    '90% of the expected price! '
                    'You must reduce the expected price '
                    'if you want to accept this offer.'
                )
