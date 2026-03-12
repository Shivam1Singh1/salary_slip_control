app_name = "salary_slip_control"
app_title = "Salary Slip Control"
app_publisher = "Shivam Singh"
app_description = "Custom hide permission for Salary Slip"
app_email = "shivam.singh@microcrispr.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "salary_slip_control",
# 		"logo": "/assets/salary_slip_control/logo.png",
# 		"title": "Salary Slip Control",
# 		"route": "/salary_slip_control",
# 		"has_permission": "salary_slip_control.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/salary_slip_control/css/salary_slip_control.css"

app_include_js = [
<<<<<<< HEAD
    "/assets/salary_slip_control/js/permission_manager_patch.js"
=======
    "/assets/salary_slip_control/salary_slip_control/js/permission_manager_patch.js"
>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346
]

# include js, css files in header of web template
# web_include_css = "/assets/salary_slip_control/css/salary_slip_control.css"
# web_include_js = "/assets/salary_slip_control/js/salary_slip_control.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "salary_slip_control/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page": "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype": "public/js/doctype.js"}
# doctype_list_js = {"doctype": "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype": "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype": "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "salary_slip_control/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# website_generators = ["Web Page"]

# Jinja
# ----------

# jinja = {
# 	"methods": "salary_slip_control.utils.jinja_methods",
# 	"filters": "salary_slip_control.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "salary_slip_control.install.before_install"
# after_install = "salary_slip_control.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "salary_slip_control.uninstall.before_uninstall"
# after_uninstall = "salary_slip_control.uninstall.after_uninstall"

# Integration Setup
# ------------------

# before_app_install = "salary_slip_control.utils.before_app_install"
# after_app_install = "salary_slip_control.utils.after_app_install"

# Integration Cleanup
# -------------------

# before_app_uninstall = "salary_slip_control.utils.before_app_uninstall"
# after_app_uninstall = "salary_slip_control.utils.after_app_uninstall"

# Desk Notifications
# ------------------

# notification_config = "salary_slip_control.notifications.get_notification_config"

# Permissions
# -----------

permission_query_conditions = {
    "Salary Slip": "salary_slip_control.overrides.salary_slip.get_permission_query_conditions"
}

has_permission = {
    "Salary Slip": "salary_slip_control.overrides.salary_slip.has_permission"
}

# DocType Class
# ---------------

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"salary_slip_control.tasks.all"
# 	],
# 	"daily": [
# 		"salary_slip_control.tasks.daily"
# 	],
# 	"hourly": [
# 		"salary_slip_control.tasks.hourly"
# 	],
# 	"weekly": [
# 		"salary_slip_control.tasks.weekly"
# 	],
# 	"monthly": [
# 		"salary_slip_control.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "salary_slip_control.install.before_tests"

# Overriding Methods
# ------------------------------

override_whitelisted_methods = {
    "frappe.core.page.permission_manager.permission_manager.update":
        "salary_slip_control.overrides.permission_manager.update",
<<<<<<< HEAD

    "attendee_life_cycle_custom.custom_scripts.salary_slip.share_doc_with_permission":
        "salary_slip_control.overrides.salary_slip.share_doc_with_permission",

    "attendee_life_cycle_custom.custom_scripts.salary_slip.set_employee_name_on_salary_slip":
        "salary_slip_control.overrides.salary_slip.set_employee_name_on_salary_slip",
}

# Fixtures
# ------------------------------
=======
    "frappe.core.page.permission_manager.permission_manager.get_permissions":
        "salary_slip_control.overrides.permission_manager.get_permissions",
}

# Fixtures
# --------
>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346

fixtures = [
    {
        "dt": "Custom Field",
<<<<<<< HEAD
        "filters": [["dt", "=", "DocPerm"], ["fieldname", "=", "hide"]]
    }
]

=======
        "filters": [["dt", "=", "Custom DocPerm"], ["fieldname", "=", "hide"]]
    }
]


>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346
# override_doctype_dashboards = {
# 	"Task": "salary_slip_control.task.get_dashboard_data"
# }

# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------

# before_request = ["salary_slip_control.utils.before_request"]
# after_request = ["salary_slip_control.utils.after_request"]

# Job Events
# ----------

# before_job = ["salary_slip_control.utils.before_job"]
# after_job = ["salary_slip_control.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = []

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"salary_slip_control.auth.validate"
# ]

# export_python_type_annotations = True

# default_log_clearing_doctypes = {}

# Translation
# ------------

# ignore_translatable_strings_from = []