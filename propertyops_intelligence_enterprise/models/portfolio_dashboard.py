# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PiePortfolioDashboard(models.Model):
    _name = "pie.portfolio.dashboard"
    _description = "Portfolio Dashboard"
    _order = "period desc, id"

    name = fields.Char(string="Dashboard Name", required=True)
    period = fields.Char(string="Period", required=True, help="e.g. 2025-Q1")
    total_properties = fields.Integer(string="Total Properties")
    total_units = fields.Integer(string="Total Units")
    occupied_units = fields.Integer(string="Occupied Units")
    occupancy_rate = fields.Float(
        string="Occupancy Rate (%)",
        compute="_compute_occupancy_rate",
        store=True,
    )
    total_rent_roll = fields.Monetary(string="Total Rent Roll", currency_field="currency_id")
    delinquent_amount = fields.Monetary(string="Delinquent Amount", currency_field="currency_id")
    maintenance_backlog = fields.Integer(string="Maintenance Backlog (open work orders)")
    noi_proxy = fields.Monetary(string="NOI Proxy", currency_field="currency_id")
    ai_vacancy_forecast = fields.Text(string="AI Vacancy Forecast")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    @api.depends("total_units", "occupied_units")
    def _compute_occupancy_rate(self):
        for rec in self:
            if rec.total_units:
                rec.occupancy_rate = (rec.occupied_units / rec.total_units) * 100.0
            else:
                rec.occupancy_rate = 0.0
