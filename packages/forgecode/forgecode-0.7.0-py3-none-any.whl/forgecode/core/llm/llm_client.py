from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class LLMCodeGenerationError(Exception):
    """Exception raised when the LLM fails to generate valid code.
    
    This can occur due to:
    - Invalid API key
    - Insufficient funds
    - Model incapable of structured generation/Invalid schema formatting
    """
    pass

class LLMClient(ABC):
    """Abstract base class for LLM clients.
    
    Implementations must support structured outputs by accepting an optional JSON schema.
    When a schema is provided, the response must conform strictly to it.
    """
    
    @abstractmethod
    def request_completion(self, model: str, messages: List[Any], schema: Optional[Dict[str, Any]] = None) -> Any:
        """Sends a list of messages to the specified LLM model and returns the response."""
        pass