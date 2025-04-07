import time
import uuid
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TraceEvent:
    """追踪事件类"""
    event_id: str
    event_type: str
    timestamp: float
    data: Dict[str, Any]
    parent_id: Optional[str] = None
    trace_id: Optional[str] = None

@dataclass
class Trace:
    """追踪类"""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    events: List[TraceEvent] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None

    def add_event(self, event_type: str, data: Dict[str, Any], parent_id: Optional[str] = None) -> TraceEvent:
        """
        添加追踪事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
            parent_id: 父事件ID
            
        Returns:
            TraceEvent: 追踪事件
        """
        event = TraceEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=time.time(),
            data=data,
            parent_id=parent_id,
            trace_id=self.trace_id
        )
        self.events.append(event)
        return event

    def end(self) -> None:
        """结束追踪"""
        self.end_time = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 追踪数据
        """
        return {
            "trace_id": self.trace_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.end_time - self.start_time if self.end_time else None,
            "events": [
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "timestamp": event.timestamp,
                    "data": event.data,
                    "parent_id": event.parent_id,
                    "trace_id": event.trace_id
                }
                for event in self.events
            ]
        }

class TraceManager:
    """追踪管理器类"""
    def __init__(self):
        self.traces: Dict[str, Trace] = {}

    def start_trace(self) -> Trace:
        """
        开始新的追踪
        
        Returns:
            Trace: 追踪对象
        """
        trace = Trace()
        self.traces[trace.trace_id] = trace
        return trace

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """
        获取追踪对象
        
        Args:
            trace_id: 追踪ID
            
        Returns:
            Optional[Trace]: 追踪对象
        """
        return self.traces.get(trace_id)

    def end_trace(self, trace_id: str) -> Optional[Trace]:
        """
        结束追踪
        
        Args:
            trace_id: 追踪ID
            
        Returns:
            Optional[Trace]: 追踪对象
        """
        trace = self.traces.get(trace_id)
        if trace:
            trace.end()
        return trace

    def clear_traces(self) -> None:
        """清除所有追踪"""
        self.traces.clear() 