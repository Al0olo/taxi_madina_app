import frappe

@frappe.whitelist(allow_guest=True,methods=["PUT"])
def cancel_request(request_id):
    try:
        trip = frappe.get_doc("Trips",{request_id})
        trip.status = "Canceled"
        trip.save(ignore_permissions=True)
        return {
            "status_code": 200,
            "message": "Success",
            "data": trip,
        }
    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {
            "status_code":400,
            "message": str(e),
            "data": {}
        }