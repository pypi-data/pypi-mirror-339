# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EmployeeOtherDutiesAssignmentType(models.Model):
    _name = "employee_other_duties_assignment_type"
    _description = "Employee Other Duties Assignment Types"
    _inherit = [
        "mixin.master_data",
    ]
