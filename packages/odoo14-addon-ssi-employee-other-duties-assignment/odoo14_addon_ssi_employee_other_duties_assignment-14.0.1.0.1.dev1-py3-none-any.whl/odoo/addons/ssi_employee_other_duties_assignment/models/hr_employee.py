# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    other_duties_assignment_ids = fields.One2many(
        string="Other Duties Assignments",
        comodel_name="employee_other_duties_assignment",
        inverse_name="employee_id",
        readonly=True,
    )
    extra_job_description_ids = fields.Many2many(
        string="Extra Job Description",
        comodel_name="job_description",
        compute="_compute_extra_job_description_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "other_duties_assignment_ids",
        "other_duties_assignment_ids.state",
    )
    def _compute_extra_job_description_ids(self):
        EODA = self.env["employee_other_duties_assignment"]
        for record in self:
            criteria = [
                ("employee_id", "=", record.id),
                ("state", "=", "open"),
            ]
            result = EODA.search(criteria).mapped("job_description_ids")
            record.extra_job_description_ids = result
