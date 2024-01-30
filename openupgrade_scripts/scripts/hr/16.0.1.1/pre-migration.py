# Copyright 2023 Coop IT Easy (https://coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_moved_fields = [
    "__last_update",
    "_order",
    "display_name",
    "name",
]

_xmlid_renames = [
    (
        "hr_contract.access_hr_contract_type_manager",
        "hr.access_hr_contract_type_manager",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.update_module_moved_models(
        env.cr, "hr.contract.type", "hr_contract", "hr"
    )
    openupgrade.update_module_moved_fields(
        env.cr, "hr.contract.type", _moved_fields, "hr_contract", "hr"
    )
    openupgrade.rename_xmlids(env.cr, _xmlid_renames)
    # Backup Many2many relation between hr.plan and hr.plan.activity.type
    openupgrade.remove_tables_fks(env.cr, ["hr_plan_hr_plan_activity_type_rel"])
    # get_legacy_name cannot be used here, because there is confilct in
    # renaming constrains on this table. Waiting for a fix in
    # openupgradelib, we will fix a new table name here.
    openupgrade.rename_tables(
        env.cr,
        [
            (
                "hr_plan_hr_plan_activity_type_rel",
                "ou_legacy_16_0_hr_plan_hr_plan_activity_type_rel",
            )
        ],
    )
