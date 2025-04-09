
from typing import Optional
from rxinferclient.api_client import ApiClient

class RxInferClient:
    """High-level client for the RxInfer API.
    
    This class provides a more user-friendly interface to the RxInfer API,
    wrapping the auto-generated client code.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the RxInfer client.
        
        Parameters:
            api_key: Optional API key for authentication. If not provided,
                    the client will attempt to use the RXINFER_API_KEY environment
                    variable or look for it in the configuration file.

        """
        self._api_client = ApiClient()
        self._api_client.configuration.access_token = api_key