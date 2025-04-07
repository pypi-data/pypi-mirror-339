from enum import Enum
from typing import Optional, Dict, Any, AsyncIterator
import json

class StreamEventType(Enum):
    """流式事件类型"""
    MESSAGE = "message"  # 消息事件
    ERROR = "error"     # 错误事件
    DONE = "done"       # 完成事件

class StreamEvent:
    """流式事件"""
    def __init__(
        self,
        event: StreamEventType,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        self.event = event
        self.data = data
        self.error = error

class StreamResponse:
    """流式响应"""
    def __init__(self, response):
        self.response = response

    async def __aiter__(self) -> AsyncIterator[StreamEvent]:
        async for line in self.response.content:
            if line:
                try:
                    data = json.loads(line)
                    event_type = StreamEventType(data.get("event", "message"))
                    if event_type == StreamEventType.ERROR:
                        yield StreamEvent(
                            event=event_type,
                            error=data.get("error")
                        )
                    else:
                        yield StreamEvent(
                            event=event_type,
                            data=data.get("data")
                        )
                except json.JSONDecodeError:
                    continue 