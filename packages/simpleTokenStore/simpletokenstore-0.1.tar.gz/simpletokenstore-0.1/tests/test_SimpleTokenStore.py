from simpleTokenStore import SimpleTokenStore
from unittest import TestCase
from datetime import datetime, timedelta
import json
import os
from unittest.mock import patch

class TestSimpleTokenStore(TestCase):
    
    ### --- is_fresh tests --- 
    def test_is_fresh_false(self):
        """
        #### Function:
            - SimpleTokenStore.TimeTokenBlock.is_fresh
        #### Inputs:
            -@time_token_block: TimeTokenBlock with creation time 2 hours in the past, and expires_in_minutes = 60
        #### Expected Behaviour:
            - the time_since_creation is > (now - timestamp), so False is returned
        #### Assertions:
            - Returned value is False
        """
        input_block = SimpleTokenStore.TimeTokenBlock(token='token',
                                                      timestamp=datetime.now() - timedelta(hours=2),
                                                      expires_in_minutes=60)
        assert(input_block.is_fresh() == False)
    
    def test_is_fresh_true(self):
        """
        #### Function:
            - SimpleTokenStore.TimeTokenBlock.is_fresh
        #### Inputs:
            -@time_token_block: TimeTokenBlock with creation time 1 hour in the past, and expires_in_minutes = 60
        #### Expected Behaviour:
            - The time_since_creation is < (now - timestamp), so True is returned
        #### Assertions:
            - Returned value is True
        """
        input_block = SimpleTokenStore.TimeTokenBlock(token='token',
                                                      timestamp=datetime.now() - timedelta(hours=1),
                                                      expires_in_minutes=120)
        assert(input_block.is_fresh() == True)
        
        
    ### --- load_token-store tests ---
    def test_load_token_store(self):
        """
        #### Function:
            - SimpleTokenStore.load_token_store
        #### Expected Behaviour:
            - the file is opened, the json is loaded and looped through to create a dict of TimeTokenBlocks that are returned
        #### Assertions:
            - the saved token data is returned in TimeTokenBlock form
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        token_dict = {'key1': {'token': 'token1', 'timestamp': timestamp, 'expires_in_minutes': 15 },
                      'key2': {'token': 'token2', 'timestamp': timestamp, 'expires_in_minutes': 30}}
        with open('test_token_store.json', 'w') as w:
            json.dump(token_dict, w)
        resp = SimpleTokenStore.load_token_store('test_token_store.json')
        os.remove('test_token_store.json')
        expected_resp1 = SimpleTokenStore.TimeTokenBlock(token='token1', 
                                                         timestamp=timestamp,
                                                         expires_in_minutes=15)
        expected_resp2 = SimpleTokenStore.TimeTokenBlock(token='token2',
                                                         timestamp=timestamp,
                                                         expires_in_minutes=30)
        expected1_dict = expected_resp1.__dict__
        returned1_dict = resp['key1'].__dict__
        for key, value in expected1_dict.items():
            assert(returned1_dict[key] == value)
            
        expected2_dict = expected_resp2.__dict__
        returned2_dict = resp['key2'].__dict__
        for key, value in expected2_dict.items():
            assert(returned2_dict[key] == value)
            
            
    ### --- save_token_to_store tests ---
    
    def test_save_token_to_store_missing(self):
        """
        #### Function:
            - SimpleTokenStore.save_token_store
        #### Inputs:
            -@token: 'test token'
            -@token_key: 'token_key'
        #### Expected Behaviour:
            - The self.store_path doesn't have a file in it, so the existing_data isn't filled 
            - new token is stored into the existing_data in 'token_key' and the json is stored in self.store_path
        #### Assertions:
            - the expected json is dumped into the self.store_path
        """
        resource = SimpleTokenStore(get_new_token_function=lambda x: 'test')
        resource.save_token_to_store(token='test token', token_key='token_key')
        data = {}
        with open(resource.store_path, 'r') as r:
            data = json.load(r)
        os.remove(resource.store_path)
        assert(data == {'token_key': {'token': 'test token', 
                                      'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      'expires_in_minutes': 30}})
        
    def test_save_token_to_store_existing_empty(self):
        """
        #### Function:
            - SimpleTokenStore.save_token_store
        #### Inputs:
            -@token: 'test token'
            -@token_key: 'token_key'
        #### Expected Behaviour:
            - The self.store_path does have a file in it, but it's empty of data 
            - the json load fails, but the exception is caught and the existing_data remains an empty dict
            - The input token is stored as a token block in the existing_data and dumped to the store_path
        #### Assertions:
            - the expected token is stored in the store_path
        """
        resource = SimpleTokenStore(get_new_token_function=lambda x: 'test')
        with open(resource.store_path, 'w') as w:
            w.write('')
        resource.save_token_to_store(token='test token', token_key='token_key')
        data = {}
        with open(resource.store_path, 'r') as r:
            data = json.load(r)
        os.remove(resource.store_path)
        assert(data == {'token_key': {'token': 'test token', 
                                      'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      'expires_in_minutes': 30}})
        
    def test_save_token_to_store_existing_present(self):
        """
        #### Function:
            - SimpleTokenStore.save_token_store
        #### Inputs:
            -@token: 'test token'
            -@token_key: 'token_key'
        #### Expected Behaviour:
            - The self.store_path has a file in it and it has some token blocks stored in it 
                so it's opened and loaded into the existing_data 
            - the new token block is added into the existing_data, and that's dumped into the store_path
        #### Assertions:
            - the expected token is added to the existing tokens in the store_path
        """
        resource = SimpleTokenStore(get_new_token_function=lambda x: 'test')
        existing_data = {
            'key1': {'token': 'token1',
                     'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'expires_in_minutes': 10},
            'key2': {'token': 'token2',
                     'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'expires_in_minutes': 20}
        }
        with open(resource.store_path, 'w') as w:
            json.dump(existing_data, w)
        resource.save_token_to_store(token='test token', token_key='token_key')
        data = {}
        with open(resource.store_path, 'r') as r:
            data = json.load(r)
        os.remove(resource.store_path)
        expected_new_data = {'token_key': {'token': 'test token', 
                                      'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      'expires_in_minutes': 30}}
        assert(data == expected_new_data | existing_data)
        
    
    ### --- check_token_store tests ---
    
    def test_check_token_store_missing(self):
        """
        #### Function:
            - SimpleTokenStore.check_token_store
        #### Inputs:
            -@token_key: 'token_key'
        #### Expected Behaviour:
            - No file is found in the store_path so it returns None 
        #### Assertions:
            - The returned value is None 
        """
        resource = SimpleTokenStore()
        if(os.path.isfile(resource.store_path)):
            os.remove(resource.store_path)
        assert(resource.check_token_store('test_key') == None)
        
    def test_check_token_store_stale(self):
        """
        #### Function:
            - SimpleTokenStore.check_token_store
        #### Imputs:
            -@token_key: 'token_key'
        #### Expected Behaviour:
            - the store_path file is found and load_token_store returns the TimeTokenBlock dict
            - the dict has a token in 'token_key', but it's stale, so is_fresh returns False, so None is returned
        #### Assertions:
            - The returned value is None
        """
        token_block_data = {'token_key' : {'token': 'ttoken',
                                           'timestamp': (datetime.now()-timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                                           'expires_in_minutes':60}}
        resource = SimpleTokenStore()
        with open(resource.store_path, 'w') as w:
            json.dump(token_block_data, w)
        assert(resource.check_token_store('token_key') == None)
    
    def test_check_token_store_fresh(self):
        """
        #### Function:
            - SimpleTokenStore.check_token_store
        #### Inputs:
            -@token_key: 'token_key'
        #### Expected Behaviour:
            - the store path file is found and the load_token_store returns the TimeTokenBlock dict
            - the dict has a token in the 'token_key', and it's fresh, so is_fresh return True, so the token inside the block is returned
        #### Assertions:
            - The returned value is the token inside the TimeTokenBlock
        """
        token_block_data = {'token_key' : {'token': 'ttoken',
                                           'timestamp': (datetime.now()-timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
                                           'expires_in_minutes':100}}
        resource = SimpleTokenStore()
        with open(resource.store_path, 'w') as w:
            json.dump(token_block_data, w)
        assert(resource.check_token_store('token_key') == 'ttoken')
        
    
    ### --- collect_token tests --- 
    @patch.object(SimpleTokenStore, 'check_token_store')
    def test_collect_token_fresh(self, mock_check_token_store):
        """
        #### Function:
            - SimpleTokenStore.collect_token
        #### Inputs:
            -@token_key: 'test_token'
        #### Expected Behaviour:
            - check_token_store returns a token, so this token is returned
        """
        mock_check_token_store.return_value = 'token1'
        resource = SimpleTokenStore()
        resp = resource.collect_token('here')
        mock_check_token_store.assert_called_once()
        assert(resp == 'token1')
        
    @patch.object(SimpleTokenStore, 'check_token_store')
    def test_collect_token_stale(self, mock_check_token_store):
        """
        #### Function:
            - SimpleTokensStore.collect_token
        #### Inputs:
            -@token_key: 'test_token'
        #### Expected Behaviour:
            - check_token_store None, so a call to get_new_token_function is made,
                this returns a token so it's stored under test_token and then returned
        #### Assertions:
            - The value returned from get_new_token_function is returned by collect_token
            - the value returned from get_new_token_function is saved into the token store under 'test_token'
        """
        mock_check_token_store.return_value = None
        resource = SimpleTokenStore()
        def new_token():
            return('new token')
        resource.get_new_token_function = new_token
        resp = resource.collect_token('test_token')
        assert(resp == 'new token')        
        data = {}
        with open(resource.store_path, 'r') as r:
            data = json.load(r)
        os.remove(resource.store_path)
        assert(data['test_token']['token'] == 'new token')
        
        
        
        
        