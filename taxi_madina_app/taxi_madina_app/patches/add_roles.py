import frappe

def add_roles(new_roles):
    for new_role in new_roles:
        if frappe.db.exists("Role", {"role_name": new_role}):
            print("Role %s already exists" % new_role)
            role = frappe.get_doc("Role", new_role)
        else:
            role = frappe.new_doc("Role")

        role.desk_access = 1
        role.search_bar = 1
        if new_role.lower() == "lava_member":
            role.desk_access = 0
            role.search_bar = 0
        role.role_name = new_role

        role.save()

def add_role_profiles(new_role_profile, roles):
    if frappe.db.exists('Role Profile', {'role_profile': new_role_profile}):
        print(f'Role profile {new_role_profile} already exists')
        role_profile = frappe.get_doc('Role Profile', new_role_profile)
    else:
        role_profile = frappe.new_doc('Role Profile')
    role_profile.role_profile = new_role_profile
    for role in roles:
        role_profile.append('roles', {'role': role})
    role_profile.save()
    print(f'New User Role profile is added: {new_role_profile} ({role_profile.name})')