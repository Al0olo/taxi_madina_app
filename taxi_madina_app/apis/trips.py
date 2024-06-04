import frappe
import json
# Create New trip request by Client

@frappe.whitelist(allow_guest=True,methods=["POST"])
def create_new_trip_request(data):
    res = {
        "status_code": 400,
        "message":"Sucess",
        "data": {}
    }
    try:
        # Get The client data
        client = frappe.get_doc("Madina Client",{"phone_number":data["phone_number"]})
        
        # Create the trip request
        trip_request = frappe.new_doc("Trips")
        trip_request.client = client.name
        
        # Set Request type
        if data["request_type"] in ["Inside The City","Outside The City","Airports"]:
            trip_request.trip_type = data["request_type"]
        
        # Set Request Status
        trip_request.status = "Pending" # At this stage it should be pening untill some driver accepts it

        # Validate on locations that already exist in db
        if not frappe.db.exist("Locations",{"location_title":data["from_location"]}):
            res["message"] = "From Location Dosen't exist"
            res["data"] = None
            return res
        if not frappe.db.exist("Locations",{"location_title":data["to_location"]}):
            res["message"] = "To Location Dosen't exist"
            res["data"] = None
            return res
        # Set the locations (from -> to)
        trip_request.from_location = data["from_location"]
        trip_request.to_location = data["to_location"]

        # Set trip direction
        trip_request.direction = data["trip_direction"]

        # set waiting time if trip direction is two way
        if data["trip_direction"] == "Two Way":
            if data["waiting_time"] in ["1 Hour","2 Hour","3 Hour","4 Hour"]:
                trip_request.waiting_time = data["waiting_time"]
            else:
                trip_request.waiting_time = "Open"
        
        # set order time
        if data["arrival_time"] != "" or data["arrival_time"] != None:
            trip_request.time = data["arrival_time"]
        
        # set trip date
        if data["trip_date"] != "" or data["trip_date"] != None:
            trip_request.trip_date = data["trip_date"]

        # Insert the request in db
        trip_request.insert(ignore_permissions=True)

        # Set the Response
        res["message"] = "Successfully Created"
        res["status_code"] = 201
        res["data"] = {
            "request_id": trip_request.name,
            "request_status": trip_request.status,
        }
    except Exception as e:
        res["message"] = str(e)
        res["data"] = None
    return res
 
@frappe.whitelist(allow_guest=True,methods=["GET"])
def get_my_requests(data):
    res = {
        "status_code": 400,
        "message":"Sucess",
        "data": {}
    }
    try:
        data = json.dumps(data)
        
        # Check if the user is Client
        if frappe.db.exists("Madina Client",{"phone_number":data["phone_number"]}):
            user = frappe.get_doc("Madina Client",{"phone_number":data["phone_number"]}) # Get User Doc from Client Doctype
            trips = frappe.get_all("Trips",{"status":('!=',"Completed"),"client":user.name},{"*"},as_dict=1) # Get Client Trips that dosen't marked as completed
        # Check if the user is Driver
        elif frappe.db.exists("Madina Driver",{"phone_number":data["phone_number"]}):
            user = frappe.get_doc("Madina Driver",{"phone_number":data["phone_number"]}) # Get User Doc from Driver Doctype
            trips = frappe.get_all("Trips",{"status":('!=',"Completed"),"driver":user.name},{"*"},as_dict=1) # Get Driver Trips that dosen't marked as completed

        res["data"] = trips
        res["message"] = "Success"
        res["status_code"] = 200
    except Exception as e:
        res["message"] = str(e)
        res["data"] = None
    return res


@frappe.whitelist(allow_guest=True,methods=["PUT"])
def cancel_request(data):
    res = {
        "status_code": 400,
        "message":"Sucess",
        "data": {}
    }
    try:
        data = json.dumps(data)
        # Get The Trip request Doc
        trip_request = frappe.get_doc("Trips",{data["request_id"]})
        
        # Set request status to canceled
        trip_request.status = "Canceled"
        trip_request.save(ignore_permissions=True)

        # Set the response
        res["status_code"] = 300
        res["message"] = "Request Canceled Successfully"
        res["data"] = {
            "request_id": trip_request.name,
            "request_status": trip_request.status,
        }
    except Exception as e:
        res["message"] = str(e)
        res["data"] = None
    return res


@frappe.whitellist(allow_guest=True,methods=["PUT"])
def approve_trip_by_driver():
    res = {
        "status_code": 400,
        "message":"Sucess",
        "data": {}
    }
    try:
        data = json.dumps(data)

        trip_request = frappe.get_doc("Trips",{data["request_id"]})
        
        # Set request status to On Going
        trip_request.status = "On Going"

        # add car details
        driver_doc = frappe.get_doc("Madina Driver",{"phone_number":data["phone_number"]})
        trip_request.driver = driver_doc.name
        trip_request.car = driver_doc.car

        trip_request.save(ignore_permissions=True)

        # Set the response
        res["status_code"] = 300
        res["message"] = "Request Canceled Successfully"
        res["data"] = {
            "request_id": trip_request.name,
            "request_status": trip_request.status,
        }

    except Exception as e:
        res["message"] = str(e)
        res["data"] = None
    return res