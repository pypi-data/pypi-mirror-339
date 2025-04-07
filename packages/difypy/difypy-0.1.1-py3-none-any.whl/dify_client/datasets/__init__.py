from typing import Dict, Any, List, Optional
from .async_client import AsyncDatasetsClient

__all__ = ['DatasetsClient', 'AsyncDatasetsClient']

class DatasetsClient:
    def __init__(self, requester):
        self.requester = requester

    def list(self, page: int = 1, limit: int = 20) -> Dict:
        params = {
            "page": page,
            "limit": limit
        }
        return self.requester.get("/datasets", params=params)

    def get(self, dataset_id: str) -> Dict:
        return self.requester.get(f"/datasets/{dataset_id}")

    def create(self, name: str, description: Optional[str] = None) -> Dict:
        data = {
            "name": name
        }
        if description:
            data["description"] = description
        return self.requester.post("/datasets", json=data)

    def delete(self, dataset_id: str) -> Dict:
        return self.requester.delete(f"/datasets/{dataset_id}") 