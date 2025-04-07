from typing import Dict, Any, Optional
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
        files: Optional[Dict] = None
    ) -> WorkflowResponse:
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
        response = self.requester.get(f"/workflows/run/{workflow_id}")
        return WorkflowStatus(**response)

    def stop(self, task_id: str, user: str) -> Dict:
        return self.requester.post(
            f"/workflows/tasks/{task_id}/stop",
            json={"user": user}
        )

    def get_parameters(self) -> Dict:
        return self.requester.get("/parameters") 