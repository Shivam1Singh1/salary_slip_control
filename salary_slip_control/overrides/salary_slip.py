import frappe


# Checks if all Salary Slip roles assigned to the user are marked as hide=1
def _all_user_roles_hidden(user):
    user_roles = set(frappe.db.sql("SELECT role FROM `tabHas Role` WHERE parent = %s", user, pluck="role"))

    rows = frappe.db.sql("""
        SELECT role, hide FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip'
    """, as_dict=True)

    if not rows:
        return False

    hide_map = {row.role: row.hide for row in rows}
    relevant_roles = user_roles & set(hide_map.keys())

    if not relevant_roles:
        return False

    # System Manager / Administrator ko hamesha full access
    bypass_roles = {"System Manager", "Administrator"}
    if user_roles & bypass_roles:
        return False

    # Sirf wo unlisted roles count karo jo Salary Slip access de sakte hain
    salary_slip_roles = set(frappe.db.sql(
        "SELECT role FROM `tabDocPerm` WHERE parent = 'Salary Slip'", pluck="role"
    ))
    unlisted_roles = (user_roles & salary_slip_roles) - set(hide_map.keys())
    if unlisted_roles:
        return False

    return all(hide_map[role] == 1 for role in relevant_roles)


# Controls document-level access based on hidden role logic
def has_permission(doc, ptype, user):
    if not user:
        user = frappe.session.user

    if _all_user_roles_hidden(user):
        user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not user_employee:
            return False
        return doc.employee == user_employee

    hidden_roles = frappe.db.sql("""
        SELECT role FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip' AND hide = 1
    """, pluck="role")

    if not hidden_roles:
        return None

    user_roles = set(frappe.db.sql("SELECT role FROM `tabHas Role` WHERE parent = %s", user, pluck="role"))
    if not user_roles & set(hidden_roles):
        return None

    user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not user_employee:
        return None

    if doc.employee == user_employee:
        return True

    reportees = frappe.db.sql("""
        SELECT name FROM `tabEmployee` WHERE reports_to = %s
    """, user_employee, pluck="name")

    if doc.employee in reportees:
        return False

    return None


# Applies list view SQL filtering to enforce hidden role restrictions
def get_permission_query_conditions(user, doctype=None):
    if not user:
        user = frappe.session.user

    if _all_user_roles_hidden(user):
        user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not user_employee:
            return "1=0"

        escaped = frappe.db.escape(user_employee)

        # Exclude shared Salary Slips of others (DocShare bypass fix)
        shared_others = frappe.db.sql(f"""
            SELECT ds.share_name FROM `tabDocShare` ds
            INNER JOIN `tabSalary Slip` ss ON ss.name = ds.share_name
            WHERE ds.share_doctype = 'Salary Slip'
            AND ds.user = {frappe.db.escape(user)}
            AND ss.employee != {escaped}
        """, pluck="share_name")

        condition = f"`tabSalary Slip`.`employee` = {escaped}"

        if shared_others:
            others_str = ", ".join([frappe.db.escape(p) for p in shared_others])
            condition += f" AND `tabSalary Slip`.`name` NOT IN ({others_str})"

        return condition

    hidden_roles = frappe.db.sql("""
        SELECT role FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip' AND hide = 1
    """, pluck="role")

    if not hidden_roles:
        return ""

    user_roles = set(frappe.db.sql("SELECT role FROM `tabHas Role` WHERE parent = %s", user, pluck="role"))
    if not user_roles & set(hidden_roles):
        return ""

    user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not user_employee:
        return ""

    reportees = frappe.db.sql("""
        SELECT name FROM `tabEmployee` WHERE reports_to = %s
    """, user_employee, pluck="name")

    if not reportees:
        return ""

    reportees_str = ", ".join([frappe.db.escape(r) for r in reportees])

    shared_reportee_slips = frappe.db.sql(f"""
        SELECT ds.share_name FROM `tabDocShare` ds
        INNER JOIN `tabSalary Slip` ss ON ss.name = ds.share_name
        WHERE ds.share_doctype = 'Salary Slip'
        AND ds.`user` = {frappe.db.escape(user)}
        AND ss.employee IN ({reportees_str})
    """, pluck="share_name")

    condition = f"`tabSalary Slip`.`employee` NOT IN ({reportees_str})"

    if shared_reportee_slips:
        slips_str = ", ".join([frappe.db.escape(p) for p in shared_reportee_slips])
        condition += f" AND `tabSalary Slip`.`name` NOT IN ({slips_str})"

    return condition