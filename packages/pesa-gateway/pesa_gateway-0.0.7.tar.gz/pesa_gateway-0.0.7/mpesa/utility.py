import requests
from typing import JSON

class Utility:
    @classmethod
    def make_request(cls, method: str, url: str, **kwargs) -> JSON:
        try:
            response = requests.request(
                method=method,
                url=url,
                **kwargs,
                timeout=kwargs.get('timeout', 30)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ReadTimeout:
            raise Exception("Request timed out")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to the server")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP error: {e}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
