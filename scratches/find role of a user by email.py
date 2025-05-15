import apiclient
from playwright.sync_api import sync_playwright


browser = sync_playwright().start().chromium.launch(headless=False, slow_mo=100)
context = browser.new_context(base_url="https://apidev.spearline.dev/")

user_email = "qa.automation.user@spearline.com"

get_all_roles = context.request.get(
    url="v6/roles",
    headers={"x-auth-token": "17cf3ae6-8a50-4a4b-a3d8-96fd6fd46079", "x-fields": "role_id"},
    params={"page_size": "100"}
)
role_ids = [role["role_id"] for role in get_all_roles.json()["data"]]
print(role_ids)

for role_id in role_ids:

    print(f"searching role [{role_id}]")
    get_users_in_this_role = context.request.get(
        url= f"v6/roles/{role_id}/users",
        headers={"x-auth-token": "17cf3ae6-8a50-4a4b-a3d8-96fd6fd46079"},
        params={"filter": f"user.email=\"{user_email}\""}
    )
    if get_users_in_this_role.status == 200:
        if get_users_in_this_role.json()["metadata"]["record_count"] > 0:
            print(role_id)
            break
