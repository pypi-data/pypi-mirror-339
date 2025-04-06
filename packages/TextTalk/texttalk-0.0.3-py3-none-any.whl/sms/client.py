import requests
from typing import List, Optional
from .exceptions import SMSException
from .validators import PhoneNumberValidator
from .config import SMSConfig

class SMSClient:
    """
    A client for sending SMS messages using Twilio.
    """
    
    def __init__(self, config: Optional[SMSConfig] = None):
        """
        Initialize the SMS client with configuration.
        
        Args:
            config (Optional[SMSConfig]): Configuration object containing Twilio credentials.
                                        If None, will try to load from environment variables.
        """
        self.config = config or SMSConfig()
        
    def send_sms(
        self,
        to_number: str,
        message: str,
    ) -> bool:
        # Validate phone number
        to_number = PhoneNumberValidator()(to_number)
        """
        Send an SMS message.
        
        Args:
            to_number (str): The recipient's phone number (E.164 format)
            message (str): The message content
        """
        
        payload = {
            "apikey": self.config.api_key,
            "partnerID": self.config.partner_id,
            "mobile": str(to_number),
            "message": message,
            "shortcode": self.config.shortcode,
            "pass_type": "plain"
        }
        
        try:
            response = requests.post(
                url=f"{self.config.api_url}/services/sendsms/",
                headers=self.config.headers,
                json=payload,
                timeout=30
            )
            print(response.json())
            return response.status_code == 200
        except Exception as e:
            raise SMSException(f"Unexpected error while sending SMS: {str(e)}")
        
        
    def send_bulk_sms(
        self,
        message: str,
        to_numbers: List[str]
    ) -> bool:
        """
        Send a bulk SMS message to multiple recipients.
        
        Args:
            message (str): The message content
            to_numbers (List[str]): List of recipient phone numbers
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        # Validate phone numbers
        to_numbers = [PhoneNumberValidator()(number) for number in to_numbers]
        
        payload = [{
            "apikey": self.config.api_key,
            "partnerID": self.config.partner_id,
            "mobile": str(new_number),
            "message": message,
            "shortcode": self.config.shortcode,
            "pass_type": "plain"
        } for new_number in to_numbers]
        
        data = {
            "count": len(payload),
            "smslist": payload
        }
        
        try:
            response = requests.post(
                url=f"{self.config.api_url}/services/sendbulk/",
                headers=self.config.headers,
                json=data,
                timeout=30
            )
            return response.status_code == 200
        except Exception as e:
            raise SMSException(f"Unexpected error while sending bulk SMS: {str(e)}")
    