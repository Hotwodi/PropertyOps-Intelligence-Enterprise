# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PieVacancyTimeline(models.Model):
    _name = "pie.vacancy.timeline"
    _description = "Vacancy Risk Timeline"
    _order = "lease_expiry, id"

    name = fields.Char(string="Reference", required=True)
    property_id = fields.Char(string="Property")
    unit_id = fields.Char(string="Unit")
    lease_expiry = fields.Date(string="Lease Expiry")
    days_until_expiry = fields.Integer(
        string="Days Until Expiry",
        compute="_compute_days_until_expiry",
        store=True,
    )
    ai_renewal_probability = fields.Float(string="AI Renewal Probability (%)")
    ai_market_demand = fields.Float(string="AI Market Demand (0-100)")
    suggested_action = fields.Selection(
        selection=[
            ("renew_negotiate", "Renew / Negotiate"),
            ("market_listing", "Market Listing"),
            ("renovate", "Renovate"),
            ("price_adjust", "Price Adjust"),
        ],
        string="Suggested Action",
    )
    risk_level = fields.Selection(
        selection=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("critical", "Critical"),
        ],
        string="Risk Level",
        default="low",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    @api.depends("lease_expiry")
    def _compute_days_until_expiry(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.lease_expiry:
                rec.days_until_expiry = (rec.lease_expiry - today).days
            else:
                rec.days_until_expiry = 0
