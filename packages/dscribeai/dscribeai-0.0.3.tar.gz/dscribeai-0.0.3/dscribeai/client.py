from typing import Optional
import requests

from .exceptions import DScribeAIException

from .models import TranscriptionResponse, AnalyzeResponse, ErrorResponse

class DScribeAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.dscribeai.com/v1"

    def transcribe(self, post_url: str, callback_url: Optional[str] = None, timeout: Optional[float] = None) -> TranscriptionResponse:
        url = f"{self.base_url}/transcribe"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "post_url": post_url,
            "callback_url": callback_url
        }

        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if not response.ok:
            error = ErrorResponse.model_validate_json(response.text)
            raise DScribeAIException(
                error_code=error.error_code, 
                error_message=error.error_message,
                status_code=response.status_code
            )

        return TranscriptionResponse.model_validate_json(response.text)
    
    def analyze(self, post_url: str, callback_url: Optional[str] = None, timeout: Optional[float] = None) -> AnalyzeResponse:
        url = f"{self.base_url}/analyze"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "post_url": post_url,
            "callback_url": callback_url
        }

        response = requests.post(url, headers=headers, json=payload, timeout=timeout)

        if not response.ok:
            error = ErrorResponse.model_validate_json(response.text)
            raise DScribeAIException(
                error_code=error.error_code, 
                error_message=error.error_message,
                status_code=response.status_code
            )
                
        return AnalyzeResponse.model_validate_json(response.text)