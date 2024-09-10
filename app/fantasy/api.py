import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
import time


class FantasyAPI():
    def __init__(self, base_url="https://api-fantasy.llt-services.com/api/v3", max_retries=3, timeout=10):
        self.base_url = base_url
        self.max_retries = max_retries
        self.timeout = timeout

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        retries = 0
        
        while retries < self.max_retries:
            try:
                response = requests.request(method, url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response.json()
            except (HTTPError, ConnectionError, Timeout) as e:
                retries += 1
                print(f"Request failed: {e}. Retrying {retries}/{self.max_retries}...")
                time.sleep(2)
            except RequestException as e:
                print(f"Non-retryable error occurred: {e}")
                break

        raise Exception(f"Failed to call API after {self.max_retries} attempts")
    
    def get_players(self):
        return self._make_request('GET', '/players')
    
    def get_player(self, player_id):
        return self._make_request('GET', f'/player/{player_id}')
    
    def get_players_with_details(self):
        data = []
        for player in self.get_players():
            data.append(self.get_player(player['id']))

        return data