# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PieLeaseAbstraction(models.Model):
    _name = "pie.lease.abstraction"
    _description = "Lease Abstraction"
    _order = "id desc"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Reference", required=True)
    lease_id = fields.Char(string="Lease ID")
    document_file = fields.Binary(string="Lease Document", attachment=True)
    document_filename = fields.Char(string="Filename")
    abstraction_status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("completed", "Completed"),
            ("reviewed", "Reviewed"),
        ],
        string="Abstraction Status",
        default="pending",
        tracking=True,
    )
    key_dates_extracted = fields.Text(string="Key Dates Extracted")
    rent_terms_extracted = fields.Text(string="Rent Terms Extracted")
    escalation_clauses_extracted = fields.Text(string="Escalation Clauses Extracted")
    renewal_options_extracted = fields.Text(string="Renewal Options Extracted")
    deposits_extracted = fields.Text(string="Deposits Extracted")
    cam_terms_extracted = fields.Text(string="CAM Terms Extracted")
    ai_confidence = fields.Float(string="AI Confidence (%)")
    reviewed_by = fields.Many2one(comodel_name="res.users", string="Reviewed By")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    def action_set_processing(self):
        for rec in self:
            rec.abstraction_status = "processing"

    def action_set_completed(self):
        for rec in self:
            rec.abstraction_status = "completed"

    def action_set_reviewed(self):
        for rec in self:
            rec.abstraction_status = "reviewed"
            rec.reviewed_by = self.env.user
