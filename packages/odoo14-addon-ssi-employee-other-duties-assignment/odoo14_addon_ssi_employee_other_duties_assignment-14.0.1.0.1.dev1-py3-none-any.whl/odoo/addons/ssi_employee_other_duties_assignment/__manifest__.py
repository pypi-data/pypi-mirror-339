# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Employee Other Duties Assigmnent",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_terminate_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_employee_document_mixin",
        "ssi_transaction_date_duration_mixin",
        "ssi_hr_employee",
        "ssi_m2o_configurator_mixin",
    ],
    "data": [
        "ir_module_category/employee_other_duties_assignment.xml",
        "res_group/res_group_data.xml",
        "res_group/employee_other_duties_assignment.xml",
        "ir_model_access/employee_other_duties_assignment_type.xml",
        "ir_model_access/employee_other_duties_assignment.xml",
        "ir_rule/employee_other_duties_assignment.xml",
        "ir_sequence/employee_other_duties_assignment.xml",
        "sequence_template/employee_other_duties_assignment.xml",
        "approval_template/employee_other_duties_assignment.xml",
        "policy_template/employee_other_duties_assignment.xml",
        "menu.xml",
        "views/employee_other_duties_assignment_type.xml",
        "views/employee_other_duties_assignment.xml",
        "views/hr_employee.xml",
    ],
    "demo": [],
}
