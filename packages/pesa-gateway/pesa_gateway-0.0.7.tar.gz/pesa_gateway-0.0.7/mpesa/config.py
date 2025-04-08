import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class MpesaConfig:
    def __init__(
        self, 
        consumer_key: Optional[str] = None, 
        consumer_secret: Optional[str] = None, 
        shortcode: Optional[str] = None, 
        passkey: Optional[str] = None,
        callback_url:Optional[str] = None, 
        is_production: bool = False):
        
        self.consumer_key = consumer_key or os.getenv("MPESA_CONSUMER_KEY")
        self.consumer_secret = consumer_secret or os.getenv("MPESA_CONSUMER_SECRET")
        self.shortcode = shortcode or os.getenv("MPESA_SHORTCODE")
        self.passkey = passkey or os.getenv("MPESA_PASSKEY")
        self.callback_url = callback_url or os.getenv("MPESA_CALLBACK_URL")
        self.is_production = is_production
        self.production_url = 'https://api.safaricom.co.ke'
        self.sandbox_url = 'https://sandbox.safaricom.co.ke'
        self.base_url = self.production_url if self.is_production else self.sandbox_url

    @property
    def base_url(self):
        return self.production_url if self.is_production else self.sandbox_url
