# ################### packages needed #################3
#       pip install selenium==4.26.1
#       pip install dataclasses-json
#       pip install webdriver-manager

import time
from outbound.bridges.zoom_bridge import ZoomOutbound

d = {
        "bridge_url": "https://app.zoom.us/wc/7883898968/start",
        "bridge_username": "alexbudak22@gmail.com",
        "bridge_password": "Skibb343en!",
        "invitee_country_code": "+91",
        "invitee_country_name": "India",
        "invitee_phone_number": "9867441411",
        "invitee_name": "Spearline Bot",
        "invitee_join_timeout": 40,
        "call_duration": 180,
        "tag": "zoom"
    }
zoom = ZoomOutbound({})
zoom.test_bridge_call_quality(d)
