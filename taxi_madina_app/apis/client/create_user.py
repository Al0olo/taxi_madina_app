import frappe

@frappe.whitelist(methods=["POST"],allow_guest=True)
def Register(phone,name):
    try:
        user = frappe.new_doc('User')
        user.enabled = 1
        user.email = str(phone) + "@gmail.com"
        user.first_name = name
        user.mobile_no = phone
        user.role_profile_name = 'Client'
        user.user_type = 'Website User'
        user.send_welcome_email = False
        user.new_password = "Asd@123"
        user.flags.ignore_permissions = True
        user.insert()
        
        client = frappe.new_doc('Madina Client')
        client.full_name = name
        client.phone_number = phone
        client.insert(ignore_permissions = True)


        res = {
            "status_code":200,
            "message": "Success",
            "data": client
        }
        return res
    except Exception as e:
        frappe.local.response.http_status_code = 400
        return {
            "status_code":400,
            "message": str(e),
            "data": {}
        }

