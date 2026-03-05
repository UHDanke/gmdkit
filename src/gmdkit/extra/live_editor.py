# Imports
from websocket import create_connection
import json
from typing import Any, Optional

# Package Imports
from gmdkit.models.prop.gzip import ObjectString, LevelObjects
from gmdkit.models.object import ObjectList
from gmdkit.serialization.functions import compress_string

# Support for iAndyHD3's WSLiveEditor Geode Mod
# Github Link: https://github.com/iAndyHD3/WSLiveEditor

WEBSOCKET_URL = "ws://127.0.0.1:1313"

class LiveEditor(ObjectString):
    """
    A websocket client for editing a level live.
    
    Requires iAndyHD3's WSLiveEditor geode mod in order to work.
    
    Can be used as a context manager to ensure the connection is properly closed:
    
        with LiveEditor() as editor:
            editor.get_level()
            editor.add_objects(objects)
    
    Parameters
    ----------
    url : str, optional
        WebSocket URL to connect to. Defaults to WEBSOCKET_URL.
    """
        
    def __init__(self, url:str=WEBSOCKET_URL):
        self.url = url
        self.ws = None

    def connect(self):
        """
        Open the WebSocket connection.
        
        Returns
        -------
        self
            Returns self to allow chaining.
            
        Raises
        ------
        ConnectionError
            If the connection cannot be established.
        """
        try:
            self.ws = create_connection(self.url)
            return self
        except Exception as e:
            self.ws = None
            raise ConnectionError(f"Failed to connect to {self.url}") from e
    
    def close(self):
        """
        Close the WebSocket connection.
        
        Raises
        ------
        RuntimeError
            If the WebSocket is not connected.
        """
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
    
    def request(self, action:str, **kwargs:Any) -> str:
        """
        Send an action to the editor and return the response.
        
        Parameters
        ----------
        action : str
            The action to perform.
        **kwargs
            Additional payload fields to include in the request.
            
        Returns
        -------
        string: str
            The response value from the editor.
            
        Raises
        ------
        RuntimeError
            If the WebSocket is not connected, or if WSLiveEditor returns an error.
        ConnectionError
            If the message fails to send.
        """
        if not self.ws:
            raise RuntimeError("webSocket is not connected")
            
        payload = {"action": action, **kwargs}
        payload_json = json.dumps(payload)
        
        try:
            self.ws.send(payload_json)
        except Exception as e:
            raise ConnectionError("failed to send action") from e
        
        raw = self.ws.recv()
        response = json.loads(raw)
        status = response.get("status")
        
        if status == "error":
            message = response.get("message","no error message provided")
            raise RuntimeError(f"response error: {message}")
        
        if not self.ws.connected: self.ws = None
        
        return response.get("response")
            
    def get_level(self) -> LevelObjects:
        """
        Fetch the current level string from the editor and load it.
        
        Returns
        -------
        LevelObjects
            The level's objects.
        """
        self.string = compress_string(self.request("GET_LEVEL_STRING"))
        return self.load()

    def replace_level(self, save_string:bool=True, save_client:bool=False):
        """
        Push the current level string to the editor.
        
        Parameters
        ----------
        save_string : bool, optional
            If True, saves the level before sending. Defaults to True.
        save_client : bool, optional
            If True, tells WSLiveEditor to save the level before reloading. Defaults to False.
        
        Returns
        -------
        None.
        """
        self.request(
            "REPLACE_LEVEL_STRING",
            levelString=self.save() if save_string else self.string,
            save=save_client
        )
        
    def add_objects(self, objects:ObjectList, batch_size:Optional[int]=None):
        """
        Add objects to the level.
        
        Parameters
        ----------
        objects : ObjectList
            The objects to add.
        batch_size : int, optional
            Number of objects to send per request. Defaults to all at once.

        Returns
        -------
        None.
        """
        if not objects: return
        
        batch_size = batch_size or len(objects)
        
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i+batch_size]
            self.request("ADD_OBJECTS", objects=batch.to_string())
    
    def remove_objects(self, group_id:int):
        """
        Remove all objects belonging to a group from the level.
        
        Parameters
        ----------
        group_id : int
            The group ID to remove.
    
        Returns
        -------
        None.
        """
        self.request("REMOVE_OBJECTS", group=group_id)