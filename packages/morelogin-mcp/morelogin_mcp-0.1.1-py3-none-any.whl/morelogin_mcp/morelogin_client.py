import requests
from typing import Dict, Any, Optional

class MoreLoginClient:
    def __init__(self, api_key: str, base_url: str = "https://api.morelogin.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and return JSON data."""
        response.raise_for_status()
        return response.json()

    def create_profile(self, name: str, platform: str, browser: str) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/profiles",
            json={
                "name": name,
                "platform": platform,
                "browser": browser
            }
        )
        return self._handle_response(response)

    def get_profile(self, profile_id: str) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/profiles/{profile_id}")
        return self._handle_response(response)

    def update_profile(self, profile_id: str, name: Optional[str] = None,
                      platform: Optional[str] = None) -> Dict[str, Any]:
        data = {}
        if name is not None:
            data["name"] = name
        if platform is not None:
            data["platform"] = platform

        response = self.session.put(
            f"{self.base_url}/profiles/{profile_id}",
            json=data
        )
        return self._handle_response(response)

    def delete_profile(self, profile_id: str) -> Dict[str, Any]:
        response = self.session.delete(f"{self.base_url}/profiles/{profile_id}")
        return self._handle_response(response)

    def add_proxy(self, proxy_type: str, host: str, port: int,
                 username: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
        data = {
            "type": proxy_type,
            "host": host,
            "port": port
        }
        if username:
            data["username"] = username
        if password:
            data["password"] = password

        response = self.session.post(f"{self.base_url}/proxies", json=data)
        return self._handle_response(response)

    def get_proxies(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/proxies")
        return self._handle_response(response)

    def update_proxy(self, proxy_id: str, host: Optional[str] = None,
                    port: Optional[int] = None) -> Dict[str, Any]:
        data = {}
        if host is not None:
            data["host"] = host
        if port is not None:
            data["port"] = port

        response = self.session.put(
            f"{self.base_url}/proxies/{proxy_id}",
            json=data
        )
        return self._handle_response(response)

    def delete_proxy(self, proxy_id: str) -> Dict[str, Any]:
        response = self.session.delete(f"{self.base_url}/proxies/{proxy_id}")
        return self._handle_response(response)

    def create_group(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        data = {"name": name}
        if description:
            data["description"] = description

        response = self.session.post(f"{self.base_url}/groups", json=data)
        return self._handle_response(response)

    def get_groups(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/groups")
        return self._handle_response(response)

    def update_group(self, group_id: str, name: Optional[str] = None,
                    description: Optional[str] = None) -> Dict[str, Any]:
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description

        response = self.session.put(
            f"{self.base_url}/groups/{group_id}",
            json=data
        )
        return self._handle_response(response)

    def delete_group(self, group_id: str) -> Dict[str, Any]:
        response = self.session.delete(f"{self.base_url}/groups/{group_id}")
        return self._handle_response(response) 