# Imports
from websocket import create_connection
import json
from typing import Any, Optional

# Package Imports
from gmdkit.models.prop.gzip import ObjectString
from gmdkit.models.object import ObjectList

# Support for iAndyHD3's WSLiveEditor Geode Mod
# Github Link: https://github.com/iAndyHD3/WSLiveEditor

WEBSOCKET_URL = "ws://127.0.0.1:1313"

class LiveEditor(ObjectString):
        
    def __init__(self, url:str=WEBSOCKET_URL):
        self.url = url
        self.ws = None

    def connect(self):
        try:
            self.ws = create_connection(self.url)
            return self
        except Exception as e:
            self.ws = None
            raise ConnectionError(f"Failed to connect to {self.url}") from e
    
    def close(self):
        if not self.ws:
            raise RuntimeError("WebSocket is not connected")
        self.ws.close()
        self.ws = None
        
    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type:
            print(f"Error: {exc_type.__name__}: {exc_val}")
    
        return False
    
    def request(self, action:str, **kwargs:Any):
        if not self.ws:
            raise RuntimeError("WebSocket is not connected")
            
        payload = {"action": action, **kwargs}
        payload_json = json.dumps(payload)
        
        try:
            self.ws.send(payload_json)
        except Exception as e:
            raise ConnectionError("Failed to send action") from e
        
        raw = self.ws.recv()
        response = json.loads(raw)
        status = response.get("status")
        
        if status == "error":
            message = response.get("message","no error message provided")
            raise RuntimeError(f"Response error: {message}")
        
        if not self.ws.connected: self.ws = None
        
        return response.get("response")
            

    def get_level(self):
        string = self.request("GET_LEVEL_STRING")
        return self.load(string, compressed=False)


    def replace_level(self, save_string:bool=True, save_client:bool=False):
        self.request(
            "REPLACE_LEVEL_STRING",
            levelString=self.save() if save_string else self.string,
            save=save_client
        )
        
    
    def add_objects(self, objects:ObjectList, batch_size:Optional[int]=None, **kwargs:Any):
        
        if not objects: return
        
        batch_size = batch_size or len(objects)
        
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i+batch_size]
            self.request("ADD_OBJECTS", objects=batch.to_string(), **kwargs)
    
    
    def remove_objects(self, group_id:int, **kwargs:Any):
        self.request("REMOVE_OBJECTS", group=group_id, **kwargs)