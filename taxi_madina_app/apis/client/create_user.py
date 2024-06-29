import frappe

@frappe.whitelist(methods=["POST"],allow_guest=True)
def Register(user,name):
    try:
        user = frappe.new_doc('User')
        user.enabled = 1
        user.email = user + "@gmail.com"
        user.first_name = name
        user.mobile_no = user
        user.role_profile_name = 'Client'
        user.user_type = 'Website User'
        user.send_welcome_email = False
        user.new_password = "Asd@123"
        user.flags.ignore_permissions = True
        user.insert()
        
        client = frappe.new_doc('Client')
        client.full_name = name
        client.phone_number = user
        client.insert(ignore_permissions = True)


        res = {
            "status_code":200,
            "message": "Success",
            "data": user + client
        }
    except Exception as e:
        return {
            "status_code":400,
            "message": str(e),
            "data": {}
        }

