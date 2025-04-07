from typing import Optional, Dict, Any, AsyncIterator, List
from ..async_request import AsyncRequester
from ..model import WorkflowResponse, WorkflowStatusResponse, WorkflowLogsResponse, FileUploadResponse, ResponseMode
from ..stream import StreamEvent, StreamEventType
from dataclasses import dataclass
from enum import Enum

class ResponseMode(Enum):
    STREAMING = "streaming"
    BLOCKING = "blocking"

@dataclass
class FileUploadResponse:
    id: str
    name: str
    size: int
    extension: str
    mime_type: str
    created_by: str
    created_at: int

class AsyncWorkflowsClient:
    def __init__(self, requester: AsyncRequester):
        self.requester = requester

    async def run(
        self,
        inputs: Dict[str, Any],
        user: Optional[str] = None,
        response_mode: str = "blocking",
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> WorkflowResponse:
        """
        运行工作流
        
        Args:
            inputs: 输入参数
            user: 用户标识
            response_mode: 响应模式，可选值：blocking, streaming
            conversation_id: 会话ID
            user_id: 用户ID
            
        Returns:
            WorkflowResponse: 工作流响应
        """
        data = {
            "inputs": inputs,
            "response_mode": response_mode
        }
        if user:
            data["user"] = user
        if conversation_id:
            data["conversation_id"] = conversation_id
        if user_id:
            data["user_id"] = user_id
            
        response = await self.requester.post("/workflows/run", json=data)
        return WorkflowResponse(**response)

    async def stream(
        self,
        inputs: Dict[str, Any],
        user: Optional[str] = None,
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> AsyncIterator[StreamEvent]:
        """
        运行流式工作流
        
        Args:
            inputs: 输入参数
            user: 用户标识
            conversation_id: 会话ID
            user_id: 用户ID
            
        Yields:
            StreamEvent: 流式事件
        """
        data = {
            "inputs": inputs,
            "response_mode": "streaming"
        }
        if user:
            data["user"] = user
        if conversation_id:
            data["conversation_id"] = conversation_id
        if user_id:
            data["user_id"] = user_id
            
        stream = await self.requester.stream("/workflows/run", json=data)
        async for event in stream:
            yield event

    async def get_status(self, task_id: str) -> WorkflowStatusResponse:
        """
        获取工作流状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            WorkflowStatusResponse: 工作流状态响应
        """
        response = await self.requester.get(f"/workflows/tasks/{task_id}")
        return WorkflowStatusResponse(**response)

    async def stop(self, task_id: str) -> Dict:
        """
        停止工作流
        
        Args:
            task_id: 任务ID
            
        Returns:
            Dict: 响应数据
        """
        return await self.requester.post(f"/workflows/tasks/{task_id}/stop")

    async def get_logs(
        self,
        task_id: str,
        limit: int = 20,
        order: str = "desc"
    ) -> WorkflowLogsResponse:
        """
        获取工作流日志
        
        Args:
            task_id: 任务ID
            limit: 日志数量限制
            order: 排序方式，可选值：asc, desc
            
        Returns:
            WorkflowLogsResponse: 工作流日志响应
        """
        params = {
            "limit": limit,
            "order": order
        }
        response = await self.requester.get(f"/workflows/tasks/{task_id}/logs", params=params)
        return WorkflowLogsResponse(**response)

    async def upload_file(
        self,
        file_path: str,
        user: str,
        file_type: str = "document"
    ) -> FileUploadResponse:
        """
        上传文件
        
        Args:
            file_path: 文件路径
            user: 用户标识
            file_type: 文件类型
            
        Returns:
            FileUploadResponse: 文件上传响应
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'user': user,
                'type': file_type
            }
            response = await self.requester.post("/files/upload", files=files, data=data)
            return FileUploadResponse(**response)

    async def get_app_info(self) -> Dict:
        """
        获取应用信息
        
        Returns:
            Dict: 应用信息
        """
        return await self.requester.get("/info")

    async def get_app_parameters(self) -> Dict:
        """
        获取应用参数
        
        Returns:
            Dict: 应用参数
        """
        return await self.requester.get("/parameters")

    async def get_workflow_config(self) -> Dict:
        """
        获取工作流配置信息，包括：
        - 输入参数配置
        - 文件上传配置
        - 系统参数限制
        
        Returns:
            Dict: 工作流配置信息
        """
        data = await self.get_app_parameters()
        return {
            "user_input_form": data.get("user_input_form", []),  # 用户输入表单配置
            "file_upload": data.get("file_upload", {}),  # 文件上传配置
            "system_parameters": data.get("system_parameters", {})  # 系统参数
        }

    async def get_workflow_input_schema(self) -> List[Dict]:
        """
        获取工作流输入参数的结构定义
        
        Returns:
            List[Dict]: 输入参数结构列表
        """
        config = await self.get_workflow_config()
        return config.get("user_input_form", [])

    async def get_file_upload_config(self) -> Dict:
        """
        获取文件上传配置信息
        
        Returns:
            Dict: 文件上传配置
        """
        config = await self.get_workflow_config()
        return config.get("file_upload", {})

    async def get_system_parameters(self) -> Dict:
        """
        获取系统参数限制
        
        Returns:
            Dict: 系统参数配置
        """
        config = await self.get_workflow_config()
        return config.get("system_parameters", {}) 