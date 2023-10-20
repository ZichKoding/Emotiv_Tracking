import os
import sys

# Need to import the cortex module's class called Cortex from the cortex_v2 directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'cortex_v2')))
from cortex import Cortex

CLIENT_ID = os.environ.get('clientId')
CLIENT_SECRET = os.environ.get('clientSecret')
WEBSOCKET_URL = os.environ.get('WEBSOCKET_URL')
HEADSET_NAME = os.environ.get('HEADSET_NAME')
LICENSE = os.environ.get('license')

cortex = Cortex(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# open websocket connection
open_conn = cortex.open()

# request access
req_access = cortex.request_access()

# query headsets
query_headsets = cortex.query_headset()

# control device
control_device = cortex.connect_headset(HEADSET_NAME)

# authorize to get cortex token
authorize = cortex.authorize()

# create session
create_session = cortex.create_session()

# subscribe data
sub_req = cortex.sub_request(streams=['eeg', 'met'])

# get data
extract_data_labels = cortex.extract_data_labels(stream_name='eeg')


close = cortex.close()