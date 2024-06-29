import frappe

@frappe.whitelist(allow_guest=True,methods=["GET"])
def get_user_orders():
    try:
        client = frappe.session.user
        trips = frappe.get_all("Trips",{"client":client},{"*"})
        return {
            "status_code": 200,
            "message": "Success",
            "data": trips,
        }
    except Exception as e:
        return {
                "status_code":400,
                "message": str(e),
                "data": {}
            }