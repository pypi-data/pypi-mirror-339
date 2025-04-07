from typing import Dict, Any, Optional, List
from ..model import ResponseMode, WorkflowResponse, WorkflowStatus
from .async_client import AsyncWorkflowsClient

__all__ = ['WorkflowsClient', 'AsyncWorkflowsClient']

class WorkflowsClient:
    def __init__(self, requester):
        self.requester = requester

    def run(
        self,
        inputs: Dict[str, Any],
        user: str,
        response_mode: ResponseMode = ResponseMode.STREAMING,
        files: Optional[List[Dict]] = None
    ) -> WorkflowResponse:
        """
        运行工作流
        
        Args:
            inputs: 输入参数
            user: 用户标识
            response_mode: 响应模式
            files: 文件列表
            
        Returns:
            WorkflowResponse: 工作流响应
        """
        data = {
            "inputs": inputs,
            "response_mode": response_mode.value,
            "user": user
        }
        if files:
            data["files"] = files

        response = self.requester.post("/workflows/run", json=data)
        return WorkflowResponse(**response)

    def get_status(self, workflow_id: str) -> WorkflowStatus:
        """
        获取工作流状态
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            WorkflowStatus: 工作流状态
        """
        response = self.requester.get(f"/workflows/run/{workflow_id}")
        return WorkflowStatus(**response)

    def stop(self, task_id: str, user: str) -> Dict:
        """
        停止工作流
        
        Args:
            task_id: 任务ID
            user: 用户标识
            
        Returns:
            Dict: 响应数据
        """
        return self.requester.post(
            f"/workflows/tasks/{task_id}/stop",
            json={"user": user}
        )

    def get_logs(
        self,
        keyword: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict:
        """
        获取工作流日志
        
        Args:
            keyword: 搜索关键字
            status: 状态过滤
            page: 页码
            limit: 每页数量
            
        Returns:
            Dict: 日志数据
        """
        params = {
            "page": page,
            "limit": limit
        }
        
        if keyword:
            params["keyword"] = keyword
        if status:
            params["status"] = status
            
        return self.requester.get("/workflows/logs", params=params)

    def get_app_info(self) -> Dict:
        """
        获取应用信息
        
        Returns:
            Dict: 应用信息
        """
        return self.requester.get("/info")

    def get_app_parameters(self) -> Dict:
        """
        获取应用参数
        
        Returns:
            Dict: 应用参数
        """
        return self.requester.get("/parameters")

    def get_workflow_config(self) -> Dict:
        """
        获取工作流配置信息，包括：
        - 输入参数配置
        - 文件上传配置
        - 系统参数限制
        
        Returns:
            Dict: 工作流配置信息
        """
        data = self.get_app_parameters()
        return {
            "user_input_form": data.get("user_input_form", []),  # 用户输入表单配置
            "file_upload": data.get("file_upload", {}),  # 文件上传配置
            "system_parameters": data.get("system_parameters", {})  # 系统参数
        }

    def get_workflow_input_schema(self) -> List[Dict]:
        """
        获取工作流输入参数的结构定义
        
        Returns:
            List[Dict]: 输入参数结构列表
        """
        config = self.get_workflow_config()
        return config.get("user_input_form", [])

    def get_file_upload_config(self) -> Dict:
        """
        获取文件上传配置信息
        
        Returns:
            Dict: 文件上传配置
        """
        config = self.get_workflow_config()
        return config.get("file_upload", {})

    def get_system_parameters(self) -> Dict:
        """
        获取系统参数限制
        
        Returns:
            Dict: 系统参数配置
        """
        config = self.get_workflow_config()
        return config.get("system_parameters", {}) 