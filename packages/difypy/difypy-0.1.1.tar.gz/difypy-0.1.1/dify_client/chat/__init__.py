from typing import Dict, Any, Optional
from ..model import ResponseMode
from .async_client import AsyncChatClient

__all__ = ['ChatClient', 'AsyncChatClient']

class ChatClient:
    def __init__(self, requester):
        self.requester = requester

    def send_message(
        self,
        message: str,
        user: str,
        response_mode: ResponseMode = ResponseMode.STREAMING,
        conversation_id: Optional[str] = None
    ) -> Dict:
        data = {
            "inputs": {"query": message},
            "response_mode": response_mode.value,
            "user": user
        }
        if conversation_id:
            data["conversation_id"] = conversation_id

        return self.requester.post("/chat-messages", json=data) 