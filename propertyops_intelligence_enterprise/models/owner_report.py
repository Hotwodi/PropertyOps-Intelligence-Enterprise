# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PieOwnerReport(models.Model):
    _name = "pie.owner.report"
    _description = "Owner Report"
    _order = "period desc, id"

    name = fields.Char(string="Reference", required=True)
    property_id = fields.Char(string="Property")
    owner_id = fields.Char(string="Owner")
    period = fields.Char(string="Period", required=True, help="e.g. 2025-Q1")
    occupancy_rate = fields.Float(string="Occupancy Rate (%)")
    rent_collected = fields.Monetary(string="Rent Collected", currency_field="currency_id")
    delinquencies = fields.Monetary(string="Delinquencies", currency_field="currency_id")
    maintenance_spend = fields.Monetary(
        string="Maintenance Spend", currency_field="currency_id"
    )
    noi = fields.Monetary(string="NOI", currency_field="currency_id")
    capex = fields.Monetary(string="Capex", currency_field="currency_id")
    ai_performance_score = fields.Float(string="AI Performance Score (0-100)")
    generated_date = fields.Datetime(string="Generated Date", default=fields.Datetime.now)
    sent_date = fields.Datetime(string="Sent Date")
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

    def action_mark_sent(self):
        for rec in self:
            rec.sent_date = fields.Datetime.now()
