import requests
from typing import Dict, Any, Optional, List, Union
from .data.definitions import (
    CategoryScore,
    ScanToxicity,
    ContentQuality,
    GenerationParameters,
    Generation,
    TokenDetails,
    PromptTokenDetails,
    Usage,
    Parameters,
    GenerationResponse
)
from .data.chat_response import ChatGenerationResponse
from .constant.constants import (
    BASE_URL,
    HEADERS,
    OAUTH_TOKEN_URL,
    MODEL_GENERATIONS_URL,
    CHAT_GENERATION_URL,
    GRANT_TYPE,
    CONTENT_TYPE_FORM,
    CONTENT_TYPE_JSON,
    PAYLOAD_TEMPLATE
)
from .models.models import get_models, get_model_ids, is_valid_model
from .rest.chat_generation import chat_generate
from .data.chat_messages import Messages
from dotenv import load_dotenv

__all__ = ['ModelsAI', 'Messages']

class Messages:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

class ModelsAI:
    """
    Python SDK for Salesforce Einstein Models API.
    
    Provides a wrapper around the Models API for authentication and
    generating content using Salesforce Einstein Models.
    """
    
    def __init__(self):
        self._access_token = None
        self._token_type = None
        self._salesforce_domain = None
        self._base_url = BASE_URL
        load_dotenv()
    
    def authenticate(self, salesforce_domain, client_id, client_secret):
        self._salesforce_domain = salesforce_domain
        url = OAUTH_TOKEN_URL.format(salesforceDomain=salesforce_domain)
        payload = {
            "grant_type": GRANT_TYPE,
            "client_id": client_id,
            "client_secret": client_secret
        }
        headers = {
            "Content-Type": CONTENT_TYPE_FORM
        }
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self._access_token = data.get("access_token")
            self._token_type = data.get("token_type")
            return True
        else:
            print(f"Authentication failed: {response.text}")
            return False
    
    def list_models(self) -> List[Dict[str, str]]:
        """
        Get a list of available models with their details.
        
        Returns:
            List of dictionaries containing model name, ID, and description
        """
        return get_models()
    
    def generate(self, model, prompt, temperature=0.7, max_tokens=100, top_p=1.0, top_k=50, stop_sequences=None):
        if not self._access_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        if not is_valid_model(model):
            raise ValueError(f"Invalid model: {model}. Valid models are: {get_model_ids()}")

        url = MODEL_GENERATIONS_URL.format(model=model)
        headers = {
            "Authorization": f"{self._token_type} {self._access_token}",
            **HEADERS
        }
        
        payload = {
            **PAYLOAD_TEMPLATE,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "top_k": top_k
        }
        
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return GenerationResponse(response.json())
        else:
            raise Exception(f"Generation failed: {response.text}")
    
    def chat_generate(self, model, messages, temperature=0.7, max_tokens=100, top_p=1.0, top_k=50, stop_sequences=None):
        if not self._access_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        if not is_valid_model(model):
            raise ValueError(f"Invalid model: {model}. Valid models are: {get_model_ids()}")

        url = CHAT_GENERATION_URL.format(model=model)
        headers = {
            "Authorization": f"{self._token_type} {self._access_token}",
            **HEADERS
        }
        
        payload = {
            **PAYLOAD_TEMPLATE,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "top_k": top_k
        }
        
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return ChatGenerationResponse(response.json())
        else:
            raise Exception(f"Chat generation failed: {response.text}")