import requests
from typing import Dict, Any
from mpesa.exceptions import MpesaAPIError


class Utility:
    @classmethod
    def make_request(cls, method: str, url: str, **kwargs):
        response = requests.request(
            method=method, url=url, **kwargs, timeout=kwargs.get("timeout", 30)
        )
        try:
            # response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise MpesaAPIError("Invalid JSON response")
        except requests.exceptions.ReadTimeout:
            raise MpesaAPIError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise MpesaAPIError("Failed to connect to the server")
        except requests.exceptions.HTTPError as e:
            raise MpesaAPIError(f"HTTP error: {e}")
        except Exception as e:
            raise MpesaAPIError(f"Request failed: {str(e)}")
