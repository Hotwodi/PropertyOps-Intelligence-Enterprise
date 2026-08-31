# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PieArrearsWorkflow(models.Model):
    _name = "pie.arrears.workflow"
    _description = "Arrears / Collections Workflow"
    _order = "days_overdue desc, id"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Reference", required=True)
    tenant_id = fields.Char(string="Tenant")
    lease_id = fields.Char(string="Lease ID")
    amount_overdue = fields.Monetary(string="Amount Overdue", currency_field="currency_id")
    days_overdue = fields.Integer(string="Days Overdue")
    stage = fields.Selection(
        selection=[
            ("reminder_1", "Reminder 1"),
            ("reminder_2", "Reminder 2"),
            ("final_notice", "Final Notice"),
            ("payment_plan", "Payment Plan"),
            ("legal", "Legal"),
            ("resolved", "Resolved"),
        ],
        string="Stage",
        default="reminder_1",
        tracking=True,
    )
    payment_plan_amount = fields.Monetary(
        string="Payment Plan Amount", currency_field="currency_id"
    )
    ai_collection_probability = fields.Float(string="AI Collection Probability (%)")
    last_action_date = fields.Datetime(string="Last Action Date")
    state = fields.Selection(
        selection=[
            ("active", "Active"),
            ("resolved", "Resolved"),
            ("escalated", "Escalated"),
        ],
        string="State",
        default="active",
        tracking=True,
    )
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

    def action_advance_stage(self):
        stage_order = [
            "reminder_1",
            "reminder_2",
            "final_notice",
            "payment_plan",
            "legal",
            "resolved",
        ]
        for rec in self:
            if rec.stage in stage_order:
                idx = stage_order.index(rec.stage)
                if idx < len(stage_order) - 1:
                    rec.stage = stage_order[idx + 1]
                    rec.last_action_date = fields.Datetime.now()
                    if rec.stage == "resolved":
                        rec.state = "resolved"

    def action_escalate(self):
        for rec in self:
            rec.state = "escalated"
            rec.last_action_date = fields.Datetime.now()
