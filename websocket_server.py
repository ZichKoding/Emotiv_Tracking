import asyncio
import json
import time
import os
from websockets.sync.client import connect

sesh = None
cor_tok = None
websocket_url = os.environ['WEBSOCKET_URL']
client_id = os.environ['clientId']
client_secret = os.environ['clientSecret']
headset_name = os.environ['headset_name']

def create_session(cortex_token: str) -> None:
    global sesh
    crea_sess_msg = {
        "id": 5,
        "jsonrpc": "2.0",
        "method": "createSession",
        "params": {
            "cortexToken": cortex_token,
            "headset": headset_name,
            "status": "active"
        }
    }
    
    with connect(websocket_url)as websocket:
        websocket.send(json.dumps(crea_sess_msg, indent=4))
        message = websocket.recv()
        print("Session: ", message)
        # Write the output to a json file 
        with open("session.json", "w") as f:
            write_message = json.loads(message)
            json.dump(write_message, f, indent=4)
            
        
        sesh = json.loads(message)
        
        
        

def hello():
    global sesh, cor_tok
    
    request_access = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "requestAccess",
        "params": {
            "clientId": client_id,
            "clientSecret": client_secret
        }
    }
    
    query_headset = {
        "id": 2,
        "jsonrpc": "2.0",
        "method": "queryHeadsets",
        "params": {
            "id": "INSIGHT2*"
        }
    }
    
    connect_headset = {
        "id": 3,
        "jsonrpc": "2.0",
        "method": "controlDevice",
        "params": {
            "command": "connect",
            "headset": headset_name
        }
    }
        
    authorize = {
        "id": 4,
        "jsonrpc": "2.0",
        "method": "authorize",
        "params": {
            "clientId": client_id,
            "clientSecret": client_secret,
            "debit": 10
        }
    }
    
    
    with connect("wss://localhost:6868") as websocket:
        # Check if the websocket is open
        websocket.send('{"id":6,"jsonrpc":"2.0","method":"getCortexInfo"}')
        message = websocket.recv()
        # print(message)
        
        # Check if access is granted
        websocket.send(json.dumps(request_access, indent=4))
        ra_mess = websocket.recv()
        # print(ra_mess)
        
        # Query headset
        websocket.send(json.dumps(query_headset, indent=4))
        qh_mess = websocket.recv()
        # print(qh_mess)
        
        # Connect headset
        websocket.send(json.dumps(connect_headset, indent=4))
        ch_mess = websocket.recv()
        # print("Connect headset: ", ch_mess)
        
        # Authorize
        websocket.send(json.dumps(authorize, indent=4))
        auth_mess = websocket.recv()
        # print("Authorize: ", auth_mess)

        # Create session
        print(auth_mess)
        try:
            cortex_token = json.loads(auth_mess)['result']['cortexToken']
            create_session(cortex_token=cortex_token)
        except:
            print("Error: ", auth_mess)
        
        # sesh = json.loads(sesh)
        try:
            # If message says "error", "code":-32019
            if sesh['error']['code'] == -32019:
                # Query session
                query_sess_msg = {
                    "id": 7,
                    "jsonrpc": "2.0",
                    "method": "querySessions",
                    "params": {
                        "cortexToken": cortex_token
                    }
                }
                
                websocket.send(json.dumps(query_sess_msg, indent=4))
                message = websocket.recv()
                print("Query session: ", message)
                
        except:
            print("Blah blah blah")
            
        sesh = sesh['result']['id'] 
        cor_tok = cortex_token


def training(action, cortex_token, session, status):
    training_msg = {
        "id": 14,
        "jsonrpc": "2.0",
        "method": "training",
        "params": {
            "cortexToken": cortex_token,
            "detection": "mentalCommand",
            "session": session,
            "action": action,
            "status": status
        }
    }
    
    with connect("wss://localhost:6868") as websocket:
        websocket.send(json.dumps(training_msg, indent=4))
        message = websocket.recv()
        print("Training: ", message)
        
        return message

async def sub_request(cortex_token: str, session: str, stream: list):
    sub_req_msg = {
        "id": 15,
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": {
            "cortexToken": cortex_token,
            "session": session,
            "streams": [stream]
        }
    }
    
    update_req_msg = {
        "id": 16,
        "jsonrpc": "2.0",
        "method": "updateSession",
        "params": {
            "cortexToken": cortex_token,
            "session": session,
            "status": "active"
        }
    }
    
    query_sess_msg = {
        "id": 7,
        "jsonrpc": "2.0",
        "method": "querySessions",
        "params": {
            "cortexToken": cortex_token
        }
    }
    
    async with connect("wss://localhost:6868", open_timeout=35, close_timeout=35) as websocket:
        await websocket.send(json.dumps(query_sess_msg, indent=4))
        message = await websocket.recv()
        print("Query session: ", message)
        
        await websocket.send(json.dumps(update_req_msg, indent=4))
        message = await websocket.recv()
        print("Update session: ", message)
        
        await websocket.send(json.dumps(sub_req_msg, indent=4))
        message = await websocket.recv()
        print("Subscribe: ", message)
        
        # send message to json file
        print("Subscribe: ", message)
        with open("sub_req.json", "w") as f:
            message = json.loads(message)
            json.dump(message, f, indent=4)
        

if __name__ == "__main__":
    hello()
    print("Session ID: ", sesh)
    print("Cortex Token: ", cor_tok)
        
    license = os.environ['license']
