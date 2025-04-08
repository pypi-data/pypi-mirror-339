import os
from datetime import datetime, timedelta
import json
from collections.abc import Callable
from typing import Union


class SimpleTokenStore:
    
    def __init__(self, get_new_token_function: Callable = lambda x: '', 
                 store_path: str = '/tmp/token_store.json',
                 expires_in_minutes: int = 30):
        self.get_new_token_function = get_new_token_function
        self.store_path = store_path
        self.expires_in_minutes = expires_in_minutes
            
    
    class TimeTokenBlock:
        
        def __init__(self, token: str, timestamp: str|datetime, expires_in_minutes: int):
            self.token = token
            if(isinstance(timestamp, datetime)):
                self.timestamp = timestamp
            else:
                self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            self.expires_in_minutes = expires_in_minutes
        
        def is_fresh(self):
            """
            #### Expected Behaviour:
                - compares the time since the token was created and now is greater than the expires_in_minutes value
                - if > it's not fresh, return False, else True
            #### Returns:
                - True if Fresh, Else False
            #### Side Effects:
                - None 
            """
            time_since_creation = datetime.now() - self.timestamp
            return(time_since_creation < timedelta(minutes=self.expires_in_minutes))

                
    def collect_token(self, token_key: str) -> str:
        """
        #### Inputs:
            -@token_key: token to look under 
        #### Expected Behaviour:
            - use check_token_store to look for a fresh token, if found return
            - otherwise get a new token and store it, then return that new token
        #### Returns:
            - a fresh token (either found in storage or newly retrieved)
        #### Side Effects:
            - through function calls may call get_new_token_function, and modify file at store_path
        """ 
        if(test_token:=self.check_token_store(token_key)):
            return(test_token)
        else:
            fresh_token = self.get_new_token_function()
            self.save_token_to_store(fresh_token, token_key)
            return(fresh_token)
        

    def check_token_store(self, token_key: str) -> Union[str, None]: 
        """
        #### Inputs: 
            -@token_key: key to check against 
        #### Expected Behaviour:
            - If the store file exists open it and look for a token block stored in token_key
            - if it's there, and it's fresh, return true, else return None
        #### Returns:
            - str for token if found and fresh, else None
        """
        if(not os.path.isfile(self.store_path)):
            return(None)
        ttb_dict = SimpleTokenStore.load_token_store(self.store_path)
        returned_block = ttb_dict.get(token_key)
        if(returned_block != None and returned_block.is_fresh()):
            return(returned_block.token)
        else:
            return(None)

        
    def save_token_to_store(self, token: str, token_key: str) -> None: 
        """
        #### Inputs:
            -@token: token string to store 
            -@token_key: key to store the token against
        #### Expected Behaviour:
            - open the token store (from path at self.store_path) if it exists, otherwise start with empty data
            - add/overwrite the value at token_key, saving the TimeTokenBlock data there 
            - write back to the store_path file 
        #### Returns:
            - None 
        #### Side Effects:
            - Adds/overwrites value in the store_path 
        """
        existing_data = {}
        if(os.path.isfile(self.store_path)):
            with open(self.store_path, "r") as r:
                try:
                    existing_data = json.load(r)
                except:
                    pass
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        token_block = {"token": token, "timestamp": timestamp, "expires_in_minutes": self.expires_in_minutes}
        existing_data[token_key] = token_block
        with open(self.store_path, 'w') as w:
            json.dump(existing_data, w)
            
            
    @staticmethod
    def load_token_store(store_path: str) -> dict[str, TimeTokenBlock]:
        """
        #### Inputs:
            -@store_path: path to find the token store at 
        #### Expected Behaviour: 
            - (is only called if file exists, so no need to wrap in exception handling)
            - opens file at store path, loads it into json, then for each value load it into a 
                TimeTokenBlock and store it the returned dict
        #### Returns:
            - dict of TimeTokenBlocks, keys are token_keys that the tokens are stored against
        #### Side Effects:
            - None 
        """
        return_dict = {}
        with open(store_path) as store_file:
            time_token_dict = json.load(store_file)
            for key, value in time_token_dict.items():
                return_dict[key] = SimpleTokenStore.TimeTokenBlock(value['token'], value['timestamp'], value['expires_in_minutes'])
        return(return_dict)
