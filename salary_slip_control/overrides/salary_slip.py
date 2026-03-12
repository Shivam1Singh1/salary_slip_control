
import frappe


def _get_hide_map():
    """Returns a dict of {role: hide} for Salary Slip from Custom DocPerm."""
    rows = frappe.db.sql("""
        SELECT role, hide FROM `tabCustom DocPerm`
        WHERE parent = 'Salary Slip'
    """, as_dict=True)
    return {row.role: row.hide for row in rows}


def _is_user_restricted(user):
    """
    Returns True only if ALL of the user's relevant roles have hide=1.
    If even one role has hide=0 → full access → returns False.
    If user has no relevant roles in Custom DocPerm → no restriction → returns False.
    """
    hide_map = _get_hide_map()
    if not hide_map:
        return False

    user_roles = set(frappe.get_roles(user))
    relevant_roles = user_roles & set(hide_map.keys())

    if not relevant_roles:
        return False

    # Even one role with hide=0 → full access
    return all(hide_map[role] == 1 for role in relevant_roles)


def has_permission(doc, ptype, user):
    if not user:
        user = frappe.session.user

    # System Manager always gets full access
    if "System Manager" in frappe.get_roles(user):
        return None

    if not _is_user_restricted(user):
        # Not restricted → let Frappe handle default permission
        return None

    # Restricted → only allow access to own Salary Slip
    user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not user_employee:
        return False

    return doc.employee == user_employee


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user

    # System Manager always gets full access
    if "System Manager" in frappe.get_roles(user):
        return ""

    if not _is_user_restricted(user):
        # Not restricted → no extra SQL condition needed
        return ""

    # Restricted → filter list to own Salary Slip only
    user_employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not user_employee:
        return "1=0"

    escaped = frappe.db.escape(user_employee)
    return f"`tabSalary Slip`.`employee` = {escaped}"