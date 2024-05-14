from TAXI_MADINA_APP.taxi_madina_app.patches.add_roles import  add_roles,add_role_profiles


def execute():
    roles = ['Driver', 'Dashboard Admin', "Client"]
    add_roles(roles)
    add_role_profiles("Driver", ['Driver'])
    add_role_profiles("Dashboard Admin", ['Dashboard Admin'])
    add_role_profiles("Client", ['Client'])