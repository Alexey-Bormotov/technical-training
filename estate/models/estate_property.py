from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

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
