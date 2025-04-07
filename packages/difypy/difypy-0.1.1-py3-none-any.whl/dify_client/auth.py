from typing import Dict

class Auth:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } 