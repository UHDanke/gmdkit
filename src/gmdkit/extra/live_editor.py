# Imports
from websocket import create_connection
import json

# Package Imports
from gmdkit.models.prop.gzip import ObjectString
from gmdkit.models.object import ObjectList

# Support for iAndyHD3's WSLiveEditor Geode Mod
# Github Link: https://github.com/iAndyHD3/WSLiveEditor

WEBSOCKET_URL = "ws://127.0.0.1:1313"

class LiveEditor(ObjectString):
    
    ENCODED = False
    
    def __init__(
            self, 
            url:str=WEBSOCKET_URL, 
            ignore_errors:bool=False
            ):
        self.url = url
        self.ws = None
        self.ignore_errors = ignore_errors

    def connect(self):
        try:
            self.ws = create_connection(self.url)
            return self
        except Exception as e:
            self.ws = None
            raise ConnectionError(f"Failed to connect to {self.url}") from e
    
    def is_connected(self):
        status = self.ws and self.ws.connected
        
        if not status: self.ws = None
        
        return status
        
    def close(self):
        if self.ws:
             self.ws.close()
             self.ws = None
        
    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type:
            print(f"Error: {exc_type.__name__}: {exc_val}")
    
        return False
    
    def send_action(self, action,**kwargs):
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
        
        if status == "error" and not self.ignore_errors:
            message = response.get("message","no error message provided")
            raise ValueError(f"Response error: {message}")
        
        self.is_connected()
        
        return response.get("response")
            

    def get_level_string(self, **kwargs):
        self.string = self.send_action("GET_LEVEL_STRING")
        return self.load()

    def add_objects(self, objects:ObjectList, batch_size=None, **kwargs):
        
        if not objects: return
        
        batch_size = batch_size or len(objects)
        
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i+batch_size]
            self.send_action("ADD_OBJECTS", objects=batch.to_string(), **kwargs)
        
    def remove_object_group(self, group_id:int, **kwargs):
        self.send_action("REMOVE_OBJECTS", group=group_id, **kwargs)