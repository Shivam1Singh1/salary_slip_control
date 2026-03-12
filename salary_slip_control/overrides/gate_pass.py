import frappe


# Checks if all Salary Slip roles assigned to the user are marked as hide=1
def _all_user_roles_hidden(user):
    user_roles = set(frappe.get_roles(user))

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

    return all(hide_map[role] == 1 for role in relevant_roles)


# Checks if user has at least one Salary Slip role marked as hide=1
def _any_user_role_hidden(user):
    hidden_roles = frappe.db.sql("""
        SELECT role FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip' AND hide = 1
    """, pluck="role")

    if not hidden_roles:
        return False

    return bool(set(frappe.get_roles(user)) & set(hidden_roles))


# Shares document with approver unless approver has a hidden role
def share_doc_with_permission(doc, method=None):
    if not doc.approver:
        return False
    if _any_user_role_hidden(doc.approver):
        return False

    from hrms.hr.utils import share_doc_with_approver
    share_doc_with_approver(doc, doc.approver)
    return True


# Shares document with employee's leave approver unless they have a hidden role
def set_employee_name_on_salary_slip(doc, method=None):
    if not doc.emoloyee:
        return

    employee = frappe.get_doc("Employee", doc.emoloyee)

    if not employee.leave_approver:
        return False
    if _any_user_role_hidden(employee.leave_approver):
        return False

    from hrms.hr.utils import share_doc_with_approver
    share_doc_with_approver(doc, employee.leave_approver)
    return True


# Controls document-level access based on hidden role logic
def has_permission(doc, ptype, user):
    if not user:
        user = frappe.session.user

    if _all_user_roles_hidden(user):
        user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not user_employee:
            return False
        return doc.emoloyee == user_employee

    hidden_roles = frappe.db.sql("""
        SELECT role FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip' AND hide = 1
    """, pluck="role")

    if not hidden_roles:
        return None

    user_roles = set(frappe.get_roles(user))
    if not user_roles & set(hidden_roles):
        return None

    user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not user_employee:
        return None

    if doc.emoloyee == user_employee:
        return True

    reportees = frappe.db.sql("""
        SELECT name FROM `tabEmployee` WHERE reports_to = %s
    """, user_employee, pluck="name")

    if doc.emoloyee in reportees:
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
        return f"`tabSalary Slip`.`emoloyee` = {escaped}"

    hidden_roles = frappe.db.sql("""
        SELECT role FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip' AND hide = 1
    """, pluck="role")

    if not hidden_roles:
        return ""

    user_roles = set(frappe.get_roles(user))
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

    shared_reportee_passes = frappe.db.sql(f"""
        SELECT ds.share_name FROM `tabDocShare` ds
        INNER JOIN `tabSalary Slip` gp ON gp.name = ds.share_name
        WHERE ds.share_doctype = 'Salary Slip'
        AND ds.`user` = {frappe.db.escape(user)}
        AND gp.emoloyee IN ({reportees_str})
    """, pluck="share_name")

    condition = f"`tabSalary Slip`.`emoloyee` NOT IN ({reportees_str})"

    if shared_reportee_passes:
        passes_str = ", ".join([frappe.db.escape(p) for p in shared_reportee_passes])
        condition += f" AND `tabSalary Slip`.`name` NOT IN ({passes_str})"

    return condition