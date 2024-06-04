import frappe

@frappw.whitelist(allow_guest=True,methods=["GET"])
def get_locations_list(type):
    res = {
        "status_code": 400,
        "message":"Sucess",
        "data": {}
    }
    try:
        locations_list = frappe.get_all("Locations",{"location_type":type},"location_title",as_dict=1)
        res["data"] = locations_list
        res["status_code"] = 200
    except Exception as e:
        res["message"] = str(e)
        res["data"] = None
    return res