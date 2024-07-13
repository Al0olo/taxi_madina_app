import frappe

@frappe.whitelist(allow_guest=True,methods=["GET"])
def get_user_orders():
    try:
        client = frappe.session.user
        client_id = frappe.get_value("Madina Client",{"phone_number":(client.split("@")[0])},"name")
        trips = frappe.get_all("Trips",{"client":client_id},{"*"})
        return {
            "status_code": 200,
            "message": "Success",
            "data": trips,
        }
    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {
                "status_code":400,
                "message": str(e),
                "data": {}
            }