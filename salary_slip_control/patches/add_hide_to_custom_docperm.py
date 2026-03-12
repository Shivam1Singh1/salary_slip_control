import frappe

def execute():
    frappe.db.sql("""
        ALTER TABLE `tabCustom DocPerm`
        ADD COLUMN IF NOT EXISTS `hide` INT(1) NOT NULL DEFAULT 0
    """)
    frappe.db.commit()
