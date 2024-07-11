import frappe

@frappe.whitelist(allow_guest=True,methods=["GET"])
def get_locations(location_type):
    try:
        # client = frappe.session.user
        if location_type == 'Inside_City':
            locations = frappe.get_all("Locations",{"location_type":'Inside City'},{"*"})
        elif location_type == 'outside_City':
            locations = frappe.get_all("Locations",{"location_type":'outside City'},{"*"})
        elif location_type == 'AirPorts':
            locations = frappe.get_all("Locations",{"location_type":'AirPorts'},{"*"})
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