import frappe
import frappe.core.page.permission_manager.permission_manager as original


@frappe.whitelist()
def update(doctype, role, permlevel, ptype, value=0):
    if doctype == "Salary Slip" and ptype == "hide":
        frappe.db.set_value(
            "Custom DocPerm",
            {
                "parent": "Salary Slip",
                "role": role,
                "permlevel": int(permlevel)
            },
            "hide",
            int(value)
        )
        frappe.db.commit()
        frappe.clear_cache(doctype="Salary Slip")
        return

    return original.update(
        doctype=doctype,
        role=role,
        permlevel=permlevel,
        ptype=ptype,
        value=value
    )


@frappe.whitelist()
def get_permissions(doctype=None, role=None):
    perms = original.get_permissions(doctype=doctype, role=role)

    if doctype == "Salary Slip" and perms:
        rows = frappe.db.sql("""
            SELECT role, hide FROM `tabCustom DocPerm`
            WHERE parent = 'Salary Slip'
        """, as_dict=True)
        hide_map = {row.role: row.hide for row in rows}

        for p in perms:
            p["hide"] = hide_map.get(p.get("role"), 0)

    return perms