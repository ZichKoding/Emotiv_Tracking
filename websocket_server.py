import asyncio
import json
import time
from websockets.sync.client import connect



def create_session(cortex_token: str) -> None:
    crea_sess_msg = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "createSession",
        "params": {
            "cortexToken": cortex_token,
            "headset": "INSIGHT2-A3D2071D",
            "status": "active"
        }
    }
    
    with connect("wss://localhost:6868")as websocket:
        websocket.send(json.dumps(crea_sess_msg, indent=4))
        message = websocket.recv()
        print("Session: ", message)
        
        return message
        
        
        

def hello():
    request_access = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "requestAccess",
        "params": {
            "clientId": "1NpE1w9SxZA1kfZEp25oCyV4wN0VF4qqJvFE1WjQ",
            "clientSecret": "L6k0DeOGDsSFfBcemWlXrMernrQfIoQ3L2Z2KPMa00tL9WBRfIB3uwAkfbRIxYIpUlgDg9VdlM99ZK52xDXVhWwmAKDo1081jsmzJdXfmXA4JUE1DEJuIlHVpYtSpyHs"
        }
    }
    
    query_headset = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "queryHeadsets",
        "params": {
            "id": "INSIGHT2*"
        }
    }
    
    connect_headset = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "controlDevice",
        "params": {
            "command": "connect",
            "headset": "INSIGHT2-A3D2071D"
        }
    }
        
    authorize = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "authorize",
        "params": {
            "clientId": "",
            "clientSecret": "",
            "debit": 10
        }
    }
    
    
    with connect("wss://localhost:6868") as websocket:
        # Check if the websocket is open
        websocket.send('{"id":1,"jsonrpc":"2.0","method":"getCortexInfo"}')
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
        cortex_token = json.loads(auth_mess)['result']['cortexToken']
        sesh = create_session(cortex_token=cortex_token)
        
        sesh = json.loads(sesh)
        try:
            # If message says "error", "code":-32019
            if sesh['error']['code'] == -32019:
                # Query session
                query_sess_msg = {
                    "id": 1,
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
            
        return sesh['result']['id'], cortex_token


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


if __name__ == "__main__":
    sesh, cor_tok = hello()
    print("Session ID: ", sesh)
    print("Cortex Token: ", cor_tok)
    license = "62ed82fc-c654-4134-9720-82101c4d9bdc"
    isTrain = False
    training_option = ""
    exit_session = False
    
    while exit_session is False:
        prompt = input("Do you want to start session? (y/n): ")
        if prompt == 'n':
            exit_session = True
        else:
            prompt_train = input("Do you want to train? (y/n): ")
            if prompt_train == 'y':
                isTrain = True
                what_train = input("What do you want to train? (neutral/left/right): ")
                if what_train == 'neutral':
                    train = training(action=what_train, cortex_token=cor_tok, session=sesh, status="start")
                    print(train)
                    time.sleep(5)
                    train_again = input("Do you want to train neutral again? (y/n): ")
                    if train_again == 'y':
                        train = training(action=what_train, cortex_token=cor_tok, session=sesh, status="start")
                        print(train)
                        time.sleep(5)
                        train_again = input("Do you want to train neutral again? (y/n): ")
                elif what_train == 'left':
                    train = training(action=what_train, cortex_token=cor_tok, session=sesh, status="start")
                    print(train)
                    time.sleep(5)
                    train_again = input("Do you want to train left again? (y/n): ")
                    if train_again == 'y':
                        train = training(action=what_train, cortex_token=cor_tok, session=sesh, status="start")
                        print(train)
                        time.sleep(5)
                        train_again = input("Do you want to train left again? (y/n): ")
                elif what_train == 'right':
                    train = training(action=what_train, cortex_token=cor_tok, session=sesh, status="start")
                    print(train)
                    time.sleep(5)
                    train_again = input("Do you want to train right again? (y/n): ")
                    if train_again == 'y':
                        train = training(action=what_train, cortex_token=cor_tok, session=sesh, status="start")
                        print(train)
                        time.sleep(5)
                        train_again = input("Do you want to train right again? (y/n): ")
                else:
                    print("Invalid input. Please try again.")
                    continue
            elif prompt_train == 'n':
                isTrain = False
                
    # hello()