import frappe
import json

@frappe.whitelist(allow_guest=True,methods=["POST"])
def authenticate_user(data):
    
    res = {
        "status_code": 400,
        "message":"Sucess",
        "data": {}
    }
    try:
        data = json.dump(data)

        # Validate if the user is existing client
        if frappe.db.exists("Madina Client",{"phone_number":data["phone_number"]}):
            client = frappe.get_doc("Madina Client",{"phone_number":data["phone_number"]})
            if data["token"] != "" or data["token"] != None:
                client.token = data["token"]
            if data["full_name"] != "" or data["full_name"] != None:
                client.full_name = data['full_name']
            client.save(ignore_permissions=True)

            res["status_code"] = 201
            res["data"] = {
                "full_name":client.full_name,
                "phone_number": client.phone_number,
                "address": client.address,
            }
        # Validate if the user is existing driver
        elif frappe.db.exists("Madina Driver",{"phone_number":data["phone_number"]}):
            driver = frappe.get_doc("Madina Driver",{"phone_number":data["phone_number"]})
            
            res["status_code"] = 202
            res["data"] = {
                "full_name":driver.full_name,
                "phone_number":driver.phone_number,
                "car": driver.car
            }
        # Create New User of type Client
        else:
            client = frappe.new_doc("Madina Client")
            client.phone_number = data["phone_number"] # The only mandatory field
            if data["token"] != "" or data["token"] != None:
                client.token = data["token"]
            if data["full_name"] != "" or data["full_name"] != None:
                client.full_name = data['full_name']
            if data["address"] != "" or data["address"] != None:
                client.address = data['address']
            client.insert(ignore_permissions=True)
            
            res["status_code"] = 203
            res["data"] = {
                "full_name":client.full_name,
                "phone_number": client.phone_number,
                "address": client.address
            }
    except Exception as e:
        res["message"] = str(e)
        res["data"] = None
    return res