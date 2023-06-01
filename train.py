import asyncio
import json
import time
import ssl
from websockets.sync.client import connect
import websocket
import threading
from datetime import datetime


class Emotiv():
    def __init__(self, clientID, clientSecret, profile, train_action=None, train_status=None, mental_actions=None):
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.cortex_token = None
        self.session_id = None
        self.auth = None
        self.headset = None
        self.profile = profile
        self.record = None
        self.status = None
        self.train_action = train_action
        self.train_status = train_status
        self.mental_actions = mental_actions
        
        self.request_access = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "requestAccess",
            "params": {
                "clientId": self.clientID,
                "clientSecret": self.clientSecret
            }
        }
        self.query_headset = {
            "id": 2,
            "jsonrpc": "2.0",
            "method": "queryHeadsets",
            "params": {
                "id": "INSIGHT2*"
            }
        }
        self.connect_headset = {
            "id": 3,
            "jsonrpc": "2.0",
            "method": "controlDevice",
            "params": {
                "command": "connect",
                "headset": "INSIGHT2-A3D2071D"
            }
        }
        self.authorize = {
            "id": 4,
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": self.clientID,
                "clientSecret": self.clientSecret,
                "debit": 10
            }
        }
        self.create_session = {
            "id": 5,
            "jsonrpc": "2.0",
            "method": "createSession",
            "params": {
                "cortexToken": self.cortex_token,
                "headset": "INSIGHT2-A3D2071D",
                "status": "active"
            }
        }
        self.load_profile = {
            "id": 6,
            "jsonrpc": "2.0",
            "method": "setupProfile",
            "params": {
                "cortexToken": self.cortex_token,
                "profile": self.profile,
                "headset": "INSIGHT2-A3D2071D",
                "status": "load"
            }
        }
        self.subscribe_mental = {
            "id": 7,
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": self.cortex_token,
                "session": self.session_id,
                "streams": ["com", "met", "sys"]
            }
        }
        self.training = {
            "id": 8,
            "jsonrpc": "2.0",
            "method": "training",
            "params": {
                "cortexToken": self.cortex_token,
                "detection": "mentalCommand",
                "session": self.session_id,
                "action": self.train_action,
                "status": self.train_status
            }
        }
        self.get_trained_signature_actions = {
            "id": 9,
            "jsonrpc": "2.0",
            "method": "getTrainedSignatureActions",
            "params": {
                "cortexToken": self.cortex_token,
                "detection": "mentalCommand",
                "profile": self.profile
            }
        }
        self.get_mental_command_active_action = {
            "id": 10,
            "jsonrpc": "2.0",
            "method": "mentalCommandActiveAction",
            "params": {
                "cortexToken": self.cortex_token,
                "profile": self.profile,
                "status": "get"
            }
        }
        self.set_mental_command_active_action = {
            "id": 11,
            "jsonrpc": "2.0",
            "method": "mentalCommandActiveAction",
            "params": {
                "cortexToken": self.cortex_token,
                "detection": "mentalCommand",
                "session": self.session_id,
                "status": "set",
                "actions": self.mental_actions
            }
        }
        self.close_session = {
            "id": 12,
            "jsonrpc": "2.0",
            "method": "updateSession",
            "params": {
                "cortexToken": self.cortex_token,
                "session": self.session_id,
                "status": "close"
            }
        }
        
        

def on_message(ws, message):
    def run(*args):
        print(message)
        print("Message received...")
    
def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("Connection established...")
    ws.send(json.dumps(request_access))

if __name__ == "__main__":
    
    request_access = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "requestAccess",
        "params": {
            "clientId": "",
            "clientSecret": ""
        }
    }
    
    websocket.enableTrace(True)
    # ws = websocket.WebSocketApp("wss://localhost:6868/",
    #                             on_message = on_message,
    #                             on_error = on_error,
    #                             on_close = on_close)
    # ws.on_open = on_open
    
    # ws.run_forever(skip_utf8_validation=True,ping_interval=10,ping_timeout=8)
    
    # req_access = ws.send(json.dumps(request_access))
    # print(req_access)
    
    # time.sleep(5)
    # req_access = ws.send(json.dumps(request_access))
    # print(req_access)
    
    # ws.run_forever()
    
    
    url = "wss://localhost:6868"
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url, 
                                    on_message=on_message,
                                    on_open = on_open,
                                    on_error=on_error,
                                    on_close=on_close)
    threadName = "WebsockThread:-{:%Y%m%d%H%M%S}".format(datetime.utcnow())
    
    # As default, a Emotiv self-signed certificate is required.
    # If you don't want to use the certificate, please replace by the below line  by sslopt={"cert_reqs": ssl.CERT_NONE}
    sslopt={"cert_reqs": ssl.CERT_NONE}

    websock_thread = threading.Thread(target=ws.run_forever)
    websock_thread.start()
    websock_thread.join()
