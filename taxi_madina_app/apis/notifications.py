import frappe

@frappe.whitelist(allow_guest=True,methods=["POST"])
def send_push_notification(token):
    try:
        user = frappe.new_doc("User Device")
        user.device_id = token
        res = {
            "status_code": 200,
            "message": "Success",
        }
    except Exception as e:
        res = {
            "status_code": 400,
            "message": "Failed",
        }