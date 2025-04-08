import pytest
from unittest.mock import Mock, patch
from morelogin_mcp.mcp_handler import MCPHandler
from morelogin_mcp.morelogin_client import MoreLoginClient

@pytest.fixture
def client():
    return MoreLoginClient(api_key="test_api_key")

@pytest.fixture
def handler(client):
    return MCPHandler(client)

@pytest.fixture
def mock_response():
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "id": "123",
            "name": "test_profile",
            "platform": "windows",
            "browser": "chrome"
        }
    }

def test_handle_create_profile(handler, mock_response):
    with patch.object(handler.client, 'create_profile') as mock_create:
        mock_create.return_value = mock_response
        response = handler.handle_request({
            "method": "create_profile",
            "params": {
                "name": "test_profile",
                "platform": "windows",
                "browser": "chrome"
            }
        })
        assert response == mock_response
        mock_create.assert_called_once_with(
            name="test_profile",
            platform="windows",
            browser="chrome"
        )

def test_handle_get_profile(handler, mock_response):
    with patch.object(handler.client, 'get_profile') as mock_get:
        mock_get.return_value = mock_response
        response = handler.handle_request({
            "method": "get_profile",
            "params": {
                "profile_id": "123"
            }
        })
        assert response == mock_response
        mock_get.assert_called_once_with(profile_id="123")

def test_handle_update_profile(handler, mock_response):
    with patch.object(handler.client, 'update_profile') as mock_update:
        mock_update.return_value = mock_response
        response = handler.handle_request({
            "method": "update_profile",
            "params": {
                "profile_id": "123",
                "name": "new_name",
                "platform": "mac"
            }
        })
        assert response == mock_response
        mock_update.assert_called_once_with(
            profile_id="123",
            name="new_name",
            platform="mac"
        )

def test_handle_delete_profile(handler, mock_response):
    with patch.object(handler.client, 'delete_profile') as mock_delete:
        mock_delete.return_value = mock_response
        response = handler.handle_request({
            "method": "delete_profile",
            "params": {
                "profile_id": "123"
            }
        })
        assert response == mock_response
        mock_delete.assert_called_once_with(profile_id="123")

def test_handle_invalid_method(handler):
    with pytest.raises(ValueError) as exc_info:
        handler.handle_request({
            "method": "invalid_method",
            "params": {}
        })
    assert "Unsupported method" in str(exc_info.value)

def test_handle_missing_params(handler):
    with pytest.raises(ValueError) as exc_info:
        handler.handle_request({
            "method": "create_profile",
            "params": {}
        })
    assert "Missing required parameters" in str(exc_info.value)

def test_handle_invalid_params(handler):
    with pytest.raises(ValueError) as exc_info:
        handler.handle_request({
            "method": "create_profile",
            "params": {
                "invalid_param": "value"
            }
        })
    assert "Invalid parameters" in str(exc_info.value) 