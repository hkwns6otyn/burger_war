# respect judge/visualizeConsole.py
import requests
from time import sleep
import json
def urlreq():
    resp = requests.get("http://localhost:5000/warState")
    return resp.json()

def visualizeState(state_json):
    # print(type(state_json))
    print("----------------------------------------")
    time = state_json["time"] 
    print(json.dumps(state_json["time"],indent=4))
    print("----------------------------------------")
    
if __name__ == "__main__":    
    while True:        
        state = urlreq()
        visualizeState(state)
        sleep(0.5)