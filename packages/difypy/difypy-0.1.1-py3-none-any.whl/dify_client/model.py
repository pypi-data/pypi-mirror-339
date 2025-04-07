from dataclasses import dataclass
from typing import Dict, Any, Optional, List
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

@dataclass
class WorkflowResponse:
    workflow_run_id: str
    task_id: str
    data: Dict[str, Any]

@dataclass
class WorkflowStatus:
    id: str
    workflow_id: str
    status: str
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]]
    error: Optional[str]
    total_steps: int
    total_tokens: int
    created_at: int
    finished_at: Optional[int]
    elapsed_time: float 