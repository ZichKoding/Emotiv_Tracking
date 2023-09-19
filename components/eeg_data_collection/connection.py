import os
import sys

from cortex_v2.cortex import Cortex


CLIENT_ID = os.environ.get('clientId')
CLIENT_SECRET = os.environ.get('clientSecret')
WEBSOCKET_URL = os.environ.get('WEBSOCKET_URL')
HEADSET_NAME = os.environ.get('HEADSET_NAME')
LICENSE = os.environ.get('license')

cortex = Cortex(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

print(cortex)
