import json

from playwright.sync_api import sync_playwright


browser = sync_playwright().start().chromium.launch(headless=False, slow_mo=100)

context = browser.new_context(base_url="https://platform.spearline.com")
login_v5 = context.request.post(
    url="/admin/api/user/token",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "keep-alive",
            "Cookie": "after_save_action=Q2FrZQ%3D%3D.OTA4YjhmYjgyMDcwZjkwZWVjODRkNjhjMjk0YjJjMTBmNzkyMzljMmM3Yjk1MDU1NzllZjdjZDExNTVhNWVhNFKmd%2FgzpAVrgWmKJUNQoAXWr5aZxgs8hJEJnq1FkNt6"
    },
    data={
        "email": "gunjan.sheth@cyara.com",
        "password": "Password!23"
    }
)

login_response = login_v5.json()
token = login_response["data"]["token"]
print(token)

print("**********************************")
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjczMzcsImV4cCI6MTcxMDMxOTE1MX0.Bg2lm6Lh1tkbi9tOIRqM40U6OBwUp20XKbuXeP8Iytg"
# print(token)

numbers_list = context.request.get(
    url="/admin/api/number",
    params={
        "application": "1"
    },
    headers={
        "Accept": "application/json",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {token}"
    }
)

# country_list = context.request.get(
#     url="/admin/api/country_code",
#     # params={
#     #     "application": "1"
#     # },
#     headers={
#         "Accept": "application/json",
#         "Connection": "keep-alive",
#         "Authorization": f"Bearer {token}"
#     }
# )

body_html = str(numbers_list.body())
print(body_html)
i = body_html.index("</pre>{")
json_txt = body_html[i+6:]
json_txt = json_txt.replace("\\n", "")
json_txt = json_txt[:-1]

obj = json.loads(json_txt)
print(obj)
l = obj['data']
numbs = [n["number"] for n in l]
print(numbs)
print("***")
ids = [n["id"] for n in l]
print(ids)


# context = browser.new_context(base_url="https://apidev.spearline.dev")
#
# user_email = "qa.automation.user@spearline.com"
#
# filt2 = '["call_start_time >= \\"2023-03-01 00:00:00\\"","call_start_time <= \\"2023-03-31 23:59:59\\"","country.code_alpha_2 in [\\"US\\"]","status = \\"failed\\""]'
# filt = '["call_start_time >= \\"2023-04-01 00:00:00\\"","call_start_time <= \\"2023-04-30 23:59:59\\""]'
# get_all_roles = context.request.get(
#     url="v6/companies/3m/tests",
#     headers={"x-auth-token": "1d514121-be9c-49ff-87d7-ac7e35e9f3ff"},
#     params={"filter": filt2}
# )
#
# obj = get_all_roles.json()
#
# f = "[\"month in [\\\"2023-05\\\", \\\"2023-04\\\", \\\"2023-03\\\", \\\"2023-02\\\", \\\"2023-01\\\", \\\"2022-12\\\"]\", \"country_code=null\"]"
# get_all_roles = context.request.get(
#     url="v6/companies/ringcentral/reports/ranking",
#     headers={"x-auth-token": "ab6d6e74-8abc-4738-b3f2-295e2b9298bc", "x-fields": "*"},
#     params={"filter": f, "sort":"month"}
# )
# obj = get_all_roles.json()
#
# role_ids = [role["role_id"] for role in get_all_roles.json()["data"]]
# print(role_ids)
#
# for role_id in role_ids:
#
#     print(f"searching role [{role_id}]")
#     get_users_in_this_role = context.request.get(
#         url= f"v6/roles/{role_id}/users",
#         headers={"x-auth-token": "17cf3ae6-8a50-4a4b-a3d8-96fd6fd46079"},
#         params={"filter": f"user.email=\"{user_email}\""}
#     )
#     if get_users_in_this_role.status == 200:
#         if get_users_in_this_role.json()["metadata"]["record_count"] > 0:
#             print(role_id)
#             break

