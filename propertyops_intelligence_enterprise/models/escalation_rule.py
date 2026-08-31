# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PieEscalationRule(models.Model):
    _name = "pie.escalation.rule"
    _description = "Rent Escalation Rule"
    _order = "next_escalation_date, id"

    name = fields.Char(string="Rule Name", required=True)
    lease_id = fields.Char(string="Lease ID")
    escalation_type = fields.Selection(
        selection=[
            ("fixed", "Fixed"),
            ("cpi_index", "CPI Index"),
            ("step_percentage", "Step Percentage"),
            ("step_amount", "Step Amount"),
        ],
        string="Escalation Type",
        default="fixed",
        required=True,
    )
    escalation_rate = fields.Float(string="Escalation Rate (%)")
    base_year_cpi = fields.Float(string="Base Year CPI")
    current_cpi = fields.Float(string="Current CPI")
    calculated_new_rent = fields.Monetary(
        string="Calculated New Rent", currency_field="currency_id"
    )
    next_escalation_date = fields.Date(string="Next Escalation Date")
    auto_apply = fields.Boolean(string="Auto Apply", default=False)
    last_applied = fields.Datetime(string="Last Applied")
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

    def action_apply_escalation(self):
        for rec in self:
            rec.last_applied = fields.Datetime.now()

    @api.onchange("escalation_type", "escalation_rate", "base_year_cpi", "current_cpi")
    def _onchange_calculate_rent(self):
        for rec in self:
            if rec.escalation_type == "cpi_index" and rec.base_year_cpi:
                rec.escalation_rate = (
                    ((rec.current_cpi - rec.base_year_cpi) / rec.base_year_cpi) * 100.0
                    if rec.current_cpi
                    else 0.0
                )
