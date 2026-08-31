# -*- coding: utf-8 -*-
{
    "name": "PropertyOps Intelligence Enterprise: Commercial Lease Abstraction, CAM & Portfolio Analytics",
    "version": "18.0.1.0.0",
    "category": "Productivity/AI",
    "summary": "Commercial lease abstraction, CAM/NNN reconciliation, escalation rules, "
               "owner reporting, vacancy risk timeline, and arrears/collections workflow.",
    "description": """
PropertyOps Intelligence Enterprise
====================================

Commercial Lease Abstraction, CAM & Portfolio Analytics for Odoo 18.

Features
--------
* Portfolio Dashboard — occupancy, rent roll, delinquencies, maintenance backlog,
  NOI proxy and AI vacancy forecast.
* Lease Abstraction — AI-assisted extraction of key dates, rent terms, escalation
  clauses, renewal options, deposits and CAM terms from lease documents.
* CAM / NNN Reconciliation — reconcile common-area maintenance expenses against
  tenant shares with variance tracking and dispute workflow.
* Escalation Rules — fixed, CPI-index, step-percentage and step-amount escalation
  rules with auto-apply and next-escalation scheduling.
* Owner Reporting — period-based owner statements with occupancy, rent collected,
  delinquencies, maintenance spend, NOI, capex and AI performance score.
* Vacancy Timeline — per-unit vacancy risk with AI renewal probability, market
  demand, suggested action and risk level.
* Arrears Workflow — collections pipeline from reminder through legal with AI
  collection probability scoring.
""",
    "author": "SoftaiDev",
    "website": "https://softaidev.pages.dev",
    "license": "LGPL-3",
    "price": 1999.99,
    "currency": "USD",
    "application": True,
    "installable": True,
    "depends": ["base", "web", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/portfolio_dashboard_views.xml",
        "views/lease_abstraction_views.xml",
        "views/cam_reconciliation_views.xml",
        "views/escalation_rule_views.xml",
        "views/owner_report_views.xml",
        "views/vacancy_timeline_views.xml",
        "views/arrears_workflow_views.xml",
        "views/menu.xml",
    ],
    "assets": {},
    "images": ["static/description/icon.png"],
}
