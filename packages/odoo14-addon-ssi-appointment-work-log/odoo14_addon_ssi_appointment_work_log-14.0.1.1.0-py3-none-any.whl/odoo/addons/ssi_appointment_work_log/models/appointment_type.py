# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AppointmentType(models.Model):
    _name = "appointment_type"
    _inherit = [
        "appointment_type",
    ]

    work_log_analytic_account_ids = fields.Many2many(
        string="Work Log Analytic Account",
        comodel_name="account.analytic.account",
        relation="rel_appointment_type_2_work_log_aa",
        column1="type_id",
        column2="analytic_account_id",
    )
    work_log_analytic_group_ids = fields.Many2many(
        string="Work Log Analytic Group",
        comodel_name="account.analytic.group",
        relation="rel_appointment_type_2_work_log_ag",
        column1="type_id",
        column2="analytic_group_id",
    )
