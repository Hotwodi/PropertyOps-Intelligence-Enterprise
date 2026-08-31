# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PieCamReconciliation(models.Model):
    _name = "pie.cam.reconciliation"
    _description = "CAM / NNN Reconciliation"
    _order = "period desc, id"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Reference", required=True)
    property_id = fields.Char(string="Property")
    period = fields.Char(string="Period", required=True, help="e.g. 2025")
    total_cam_expenses = fields.Monetary(
        string="Total CAM Expenses", currency_field="currency_id"
    )
    tenant_share_pct = fields.Float(string="Tenant Share (%)")
    tenant_amount = fields.Monetary(
        string="Tenant Amount",
        compute="_compute_tenant_amount",
        store=True,
        currency_field="currency_id",
    )
    reconciled = fields.Boolean(string="Reconciled")
    variance = fields.Monetary(string="Variance", currency_field="currency_id")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("reconciled", "Reconciled"),
            ("disputed", "Disputed"),
            ("closed", "Closed"),
        ],
        string="State",
        default="draft",
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

    @api.depends("total_cam_expenses", "tenant_share_pct")
    def _compute_tenant_amount(self):
        for rec in self:
            rec.tenant_amount = rec.total_cam_expenses * (rec.tenant_share_pct / 100.0)

    def action_reconcile(self):
        for rec in self:
            rec.reconciled = True
            rec.state = "reconciled"

    def action_dispute(self):
        for rec in self:
            rec.state = "disputed"

    def action_close(self):
        for rec in self:
            rec.state = "closed"
