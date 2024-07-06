import frappe

@frappe.whitelist(allow_guest=True,methods=["POST"])
def create_order(from_location,to_location,trip_type,direction,waiting_time,trip_date):
    try:
        client = frappe.session.user

        trip = frappe.new_doc("Trips")
        trip.client = client
        trip.trip_type = trip_type
        trip.status = "Pending"
        trip.direction = direction
        trip.waiting_time = waiting_time
        trip.from_location = from_location
        trip.to_location = to_location
        trip.trip_date = trip_date
        trip.insert(ignore_permissions=True)

        return {
            "status_code": 200,
            "message": "Success",
            "data": trip.name
        }

    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {
            "status_code":400,
            "message": str(e),
            "data": {}
        }