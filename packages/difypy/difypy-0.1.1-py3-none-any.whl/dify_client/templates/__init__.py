from typing import Dict, Any, List, Optional

class TemplatesClient:
    def __init__(self, requester):
        self.requester = requester

    def list(self, page: int = 1, limit: int = 20) -> Dict:
        params = {
            "page": page,
            "limit": limit
        }
        return self.requester.get("/templates", params=params)

    def get(self, template_id: str) -> Dict:
        return self.requester.get(f"/templates/{template_id}")

    def create(
        self,
        name: str,
        content: str,
        description: Optional[str] = None
    ) -> Dict:
        data = {
            "name": name,
            "content": content
        }
        if description:
            data["description"] = description
        return self.requester.post("/templates", json=data)

    def update(
        self,
        template_id: str,
        name: Optional[str] = None,
        content: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict:
        data = {}
        if name:
            data["name"] = name
        if content:
            data["content"] = content
        if description:
            data["description"] = description
        return self.requester.put(f"/templates/{template_id}", json=data)

    def delete(self, template_id: str) -> Dict:
        return self.requester.delete(f"/templates/{template_id}") 