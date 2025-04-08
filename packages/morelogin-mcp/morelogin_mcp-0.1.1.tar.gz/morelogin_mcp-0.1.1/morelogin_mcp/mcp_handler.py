from typing import Dict, Any
from .morelogin_client import MoreLoginClient

class MCPHandler:
    def __init__(self, client: MoreLoginClient):
        self.client = client

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})

        if not method:
            raise ValueError("Missing method in request")

        handler = getattr(self, f"_handle_{method}", None)
        if not handler:
            raise ValueError("Unsupported method")

        if not params:
            raise ValueError("Missing required parameters")

        return handler(params)

    def _handle_create_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["name", "platform", "browser"]
        self._validate_params(params, required)
        return self.client.create_profile(
            name=params["name"],
            platform=params["platform"],
            browser=params["browser"]
        )

    def _handle_get_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["profile_id"]
        self._validate_params(params, required)
        return self.client.get_profile(profile_id=params["profile_id"])

    def _handle_update_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["profile_id"]
        self._validate_params(params, required)
        return self.client.update_profile(
            profile_id=params["profile_id"],
            name=params.get("name"),
            platform=params.get("platform")
        )

    def _handle_delete_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["profile_id"]
        self._validate_params(params, required)
        return self.client.delete_profile(profile_id=params["profile_id"])

    def _handle_add_proxy(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["type", "host", "port"]
        self._validate_params(params, required)
        return self.client.add_proxy(
            proxy_type=params["type"],
            host=params["host"],
            port=params["port"],
            username=params.get("username"),
            password=params.get("password")
        )

    def _handle_get_proxies(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.get_proxies()

    def _handle_update_proxy(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["proxy_id"]
        self._validate_params(params, required)
        return self.client.update_proxy(
            proxy_id=params["proxy_id"],
            host=params.get("host"),
            port=params.get("port")
        )

    def _handle_delete_proxy(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["proxy_id"]
        self._validate_params(params, required)
        return self.client.delete_proxy(proxy_id=params["proxy_id"])

    def _handle_create_group(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["name"]
        self._validate_params(params, required)
        return self.client.create_group(
            name=params["name"],
            description=params.get("description")
        )

    def _handle_get_groups(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.get_groups()

    def _handle_update_group(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["group_id"]
        self._validate_params(params, required)
        return self.client.update_group(
            group_id=params["group_id"],
            name=params.get("name"),
            description=params.get("description")
        )

    def _handle_delete_group(self, params: Dict[str, Any]) -> Dict[str, Any]:
        required = ["group_id"]
        self._validate_params(params, required)
        return self.client.delete_group(group_id=params["group_id"])

    def _validate_params(self, params: Dict[str, Any], required: list) -> None:
        missing = [param for param in required if param not in params]
        if missing:
            raise ValueError(f"Invalid parameters")

        invalid = [key for key in params if not isinstance(params[key], (str, int, float, bool, type(None)))]
        if invalid:
            raise ValueError(f"Invalid parameters") 