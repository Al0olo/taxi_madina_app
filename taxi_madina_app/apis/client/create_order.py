import frappe

@frappe.whitelist(allow_guest=True,methods=["POST"])
def create_order(from_location,to_location,trip_type,direction,waiting_time,trip_date,phone_num):
    try:
        client = frappe.session.user

        trip = frappe.new_doc("Trips")
        trip.client = client
        if trip_type == 'inside_city':
            trip.trip_type = "Inside The City"
        elif trip_type == 'outside_city':
            trip.trip_type = 'Outside The City'
        elif trip_type == 'airports':
            trip.trip_type = 'Airports'
        trip.status = "Pending"
        if direction == 'one_way':
            trip.direction = "One Way"
        
        trip.time = str(waiting_time) + ' Min'
        trip.from_location = from_location
        trip.to_location = to_location
        trip.estimated_time = phone_num
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