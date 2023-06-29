from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float('Price', required=True)
    state = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        default=False
    )
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_date_deadline',
        inverse='_compute_validity'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
        ondelete='cascade'
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        string='Property type',
        store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]

    @api.model
    def create(self, vals):
        if vals.get('property_id') and vals.get('price'):
            prop = self.env['estate.property'].browse(vals['property_id'])
            if prop.offer_ids:
                max_offer = max(prop.mapped('offer_ids.price'))
                if float_compare(vals['price'], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError(
                        'The offer must be higher than %.2f' % max_offer)
            prop.state = 'offer_received'
        return super().create(vals)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Datetime.now()
            record.date_deadline = (
                date +
                relativedelta(days=record.validity)
            )

    def _compute_validity(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Datetime.today()
            record.validity = (
                record.date_deadline -
                date
            ).days

    def action_accept(self):
        if 'accepted' in self.mapped('property_id.offer_ids.state'):
            raise UserError('An offer has already been accepted.')
        self.write(
            {
                'state': 'accepted'
            }
        )
        return self.mapped('property_id').write(
            {
                'state': 'offer_accepted',
                'selling_price': self.price,
                'buyer_id': self.partner_id.id
            }
        )

    def action_refuse(self):
        return self.write(
            {
                'state': 'refused'
            }
        )
