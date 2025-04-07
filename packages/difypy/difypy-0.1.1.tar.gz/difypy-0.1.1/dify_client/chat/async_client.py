from typing import Optional, Dict, Any, List, AsyncIterator
from ..async_request import AsyncRequester
from ..model import ChatResponse, ChatMessageResponse
from ..stream import StreamEvent, StreamEventType

class AsyncChatClient:
    def __init__(self, requester: AsyncRequester):
        self.requester = requester

    async def send_message(
        self,
        message: str,
        user: Optional[str] = None,
        response_mode: str = "blocking",
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None,
        files: Optional[List[Dict]] = None
    ) -> ChatResponse:
        """
        发送聊天消息
        
        Args:
            message: 消息内容
            user: 用户标识
            response_mode: 响应模式，可选值：blocking, streaming
            conversation_id: 会话ID
            user_id: 用户ID
            files: 文件列表
            
        Returns:
            ChatResponse: 聊天响应
        """
        data = {
            "message": message,
            "response_mode": response_mode
        }
        if user:
            data["user"] = user
        if conversation_id:
            data["conversation_id"] = conversation_id
        if user_id:
            data["user_id"] = user_id
        if files:
            data["files"] = files
            
        response = await self.requester.post("/chat/messages", json=data)
        return ChatResponse(**response)

    async def stream_message(
        self,
        message: str,
        user: Optional[str] = None,
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None,
        files: Optional[List[Dict]] = None
    ) -> AsyncIterator[StreamEvent]:
        """
        发送流式聊天消息
        
        Args:
            message: 消息内容
            user: 用户标识
            conversation_id: 会话ID
            user_id: 用户ID
            files: 文件列表
            
        Yields:
            StreamEvent: 流式事件
        """
        data = {
            "message": message,
            "response_mode": "streaming"
        }
        if user:
            data["user"] = user
        if conversation_id:
            data["conversation_id"] = conversation_id
        if user_id:
            data["user_id"] = user_id
        if files:
            data["files"] = files
            
        stream = await self.requester.stream("/chat/messages", json=data)
        async for event in stream:
            yield event

    async def get_messages(
        self,
        conversation_id: str,
        limit: int = 20,
        order: str = "desc"
    ) -> ChatMessageResponse:
        """
        获取聊天消息
        
        Args:
            conversation_id: 会话ID
            limit: 消息数量限制
            order: 排序方式，可选值：asc, desc
            
        Returns:
            ChatMessageResponse: 聊天消息响应
        """
        params = {
            "limit": limit,
            "order": order
        }
        response = await self.requester.get(f"/chat/conversations/{conversation_id}/messages", params=params)
        return ChatMessageResponse(**response)

    async def delete_conversation(self, conversation_id: str) -> Dict:
        """
        删除会话
        
        Args:
            conversation_id: 会话ID
            
        Returns:
            Dict: 响应数据
        """
        return await self.requester.delete(f"/chat/conversations/{conversation_id}") 