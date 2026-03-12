import frappe
import frappe.core.page.permission_manager.permission_manager as original


@frappe.whitelist()
def update(doctype, role, permlevel, ptype, value=0):
    if doctype == "Salary Slip" and ptype == "hide":
<<<<<<< HEAD
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
=======
        frappe.db.sql("""
            UPDATE `tabCustom DocPerm`
            SET hide = %s
            WHERE parent = 'Salary Slip'
            AND role = %s
            AND permlevel = %s
        """, (int(value), role, int(permlevel)))

>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346
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
<<<<<<< HEAD
        hide_map = {}
=======
>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346
        rows = frappe.db.sql("""
            SELECT role, hide FROM `tabCustom DocPerm`
            WHERE parent = 'Salary Slip'
        """, as_dict=True)
<<<<<<< HEAD
        for row in rows:
            hide_map[row.role] = row.hide
=======
        hide_map = {row.role: row.hide for row in rows}
>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346

        for p in perms:
            p["hide"] = hide_map.get(p.get("role"), 0)

<<<<<<< HEAD
    return perms
=======
    return perms
>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346
