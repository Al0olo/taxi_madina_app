import frappe
from frappe.auth import LoginManager


@frappe.whitelist(methods=["POST"],allow_guest=True)
def login(user,pwd="Asd@123"):
    try:
        user_email = user + "@gmail.com"
        login_manager = LoginManager()
        login_manager.authenticate(user=user_email, pwd=pwd)
        login_manager.post_login()
        client_doc = frappe.get_doc("Madina Client",{"phone_number":user})
        res = {
            "status_code":200,
            "message": "Success",
            "data": client_doc
        }
        return res
    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {
            "status_code":400,
            "message": str(e),
            "data": {}
        }

