import pytest
from unittest.mock import Mock, patch
from morelogin_mcp.morelogin_client import MoreLoginClient

@pytest.fixture
def client():
    return MoreLoginClient(api_key="test_api_key")

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

def test_create_profile(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.post.return_value.status_code = 200
        mock_session.return_value.post.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.create_profile(
            name="test_profile",
            platform="windows",
            browser="chrome"
        )
        assert response == mock_response
        mock_session.return_value.post.assert_called_once()

def test_get_profile(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        mock_session.return_value.get.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.get_profile(profile_id="123")
        assert response == mock_response
        mock_session.return_value.get.assert_called_once()

def test_update_profile(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.put.return_value.status_code = 200
        mock_session.return_value.put.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.update_profile(
            profile_id="123",
            name="new_name",
            platform="mac"
        )
        assert response == mock_response
        mock_session.return_value.put.assert_called_once()

def test_delete_profile(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.delete.return_value.status_code = 200
        mock_session.return_value.delete.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.delete_profile(profile_id="123")
        assert response == mock_response
        mock_session.return_value.delete.assert_called_once()

def test_add_proxy(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.post.return_value.status_code = 200
        mock_session.return_value.post.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.add_proxy(
            proxy_type="http",
            host="127.0.0.1",
            port=8080,
            username="user",
            password="pass"
        )
        assert response == mock_response
        mock_session.return_value.post.assert_called_once()

def test_get_proxies(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        mock_session.return_value.get.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.get_proxies()
        assert response == mock_response
        mock_session.return_value.get.assert_called_once()

def test_update_proxy(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.put.return_value.status_code = 200
        mock_session.return_value.put.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.update_proxy(
            proxy_id="123",
            host="new.host.com",
            port=9090
        )
        assert response == mock_response
        mock_session.return_value.put.assert_called_once()

def test_delete_proxy(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.delete.return_value.status_code = 200
        mock_session.return_value.delete.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.delete_proxy(proxy_id="123")
        assert response == mock_response
        mock_session.return_value.delete.assert_called_once()

def test_create_group(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.post.return_value.status_code = 200
        mock_session.return_value.post.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.create_group(
            name="test_group",
            description="测试分组"
        )
        assert response == mock_response
        mock_session.return_value.post.assert_called_once()

def test_get_groups(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        mock_session.return_value.get.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.get_groups()
        assert response == mock_response
        mock_session.return_value.get.assert_called_once()

def test_update_group(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.put.return_value.status_code = 200
        mock_session.return_value.put.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.update_group(
            group_id="123",
            name="new_name",
            description="新的描述"
        )
        assert response == mock_response
        mock_session.return_value.put.assert_called_once()

def test_delete_group(client, mock_response):
    with patch('requests.Session') as mock_session:
        mock_session.return_value.delete.return_value.status_code = 200
        mock_session.return_value.delete.return_value.json.return_value = mock_response
        client.session = mock_session.return_value
        response = client.delete_group(group_id="123")
        assert response == mock_response
        mock_session.return_value.delete.assert_called_once() 