import frappe

@frappe.whitelist(allow_guest=True,methods=["GET"])
def get_locations(location_type):
    try:
        # client = frappe.session.user
        locations = frappe.get_all("Locations",{"location_type":location_type},{"*"})
        return {
            "status_code": 200,
            "message": "Success",
            "data": locations,
        }
    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {
                "status_code":400,
                "message": str(e),
                "data": {}
            }