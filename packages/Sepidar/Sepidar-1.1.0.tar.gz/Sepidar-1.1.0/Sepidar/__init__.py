import requests
import json

class Sepidar:
    """
    A class for interacting with the Sepidar search API
    
    Example usage:
    >>> sepidar = Sepidar("Tatlo", page=1)
    >>> results = sepidar.search()
    >>> print(results)
    """
    
    def __init__(self,query, page=1):
        """
        Initializes the class
        
        Parameters:
            query (str): Search query
            page (int): Page number (default: 1)
            base_url (str): Base URL of the API (default: Sepidar URL)
        """
        self.base_url = "https://search.sepidar.website/api/search"
        self.query = query
        self.page = page
        import random

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User -Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/53{random.randint(1,9)}.3{random.randint(5,9)}"
        }
    
    def search(self):
        data = {
            "query": self.query,
            "page": self.page
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def set_user_agent(self, user_agent):
        """
        Set a new User-Agent for requests
        
        Parameters:
            user_agent (str): New User-Agent string
        """
        self.headers["User -Agent"] = user_agent


    def get_search_history(self):
        """
        Retrieve the search history
        
        Returns:
            list: A list of previous search queries
        """
        return getattr(self, '_search_history', [])
    
    def clear_search_history(self):
        """
        Clear the search history
        """
        self._search_history = []
    
    def search_with_history(self, query, page=1):
        """
        Perform a search and save the query to history
        
        Parameters:
            query (str): Search query
            page (int): Page number (default: 1)
            
        Returns:
            dict: JSON response from the server or None in case of error
        """
        if not hasattr(self, '_search_history'):
            self._search_history = []
        
        self._search_history.append(query)
        return self.search(query, page)