import sys  
import os  
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))  
import pytest  
from unittest.mock import patch, MagicMock  
from app import app  
from app.controller import NotifController, UserController, ReminderController  
  
@pytest.fixture  
def client():  
    app.config['TESTING'] = True  
    with app.test_client() as client:  
        yield client  
  
@pytest.fixture  
def mock_requests_post():  
    with patch('requests.post') as mock_post:  
        yield mock_post  
  
@pytest.fixture  
def mock_requests_get():  
    with patch('requests.get') as mock_get:  
        yield mock_get  
  
def test_index(client):  
    response = client.get('/')  
    assert response.status_code == 200  
    assert response.data == b'Hello Flask'  
  
def test_register(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"status": "success", "message": "User registered"}  
  
    response = client.post('/register', json={"username": "testuser", "password": "testpass"})  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "User registered"}  
  
def test_login(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"status": "success", "message": "User logged in"}  
  
    response = client.post('/login', json={"username": "testuser", "password": "testpass"})  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "User logged in"}  
  
def test_get_all_user(client, mock_requests_get):  
    mock_requests_get.return_value.status_code = 200  
    mock_requests_get.return_value.json.return_value = [{"id": 1, "username": "testuser"}]  
  
    response = client.get('/api/allUser')  
    assert response.status_code == 200  
    assert response.json == [{"id": 1, "username": "testuser"}]  
  
def test_user_by_token(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"id": 1, "username": "testuser"}  
  
    response = client.post('/user-by-token', json={"token": "testtoken"})  
    assert response.status_code == 200  
    assert response.json == {"id": 1, "username": "testuser"}  
  
def test_reminder_get(client, mock_requests_get):  
    mock_requests_get.return_value.status_code = 200  
    mock_requests_get.return_value.json.return_value = [{"id": 1, "message": "Reminder 1"}]  
  
    response = client.get('/reminder')  
    assert response.status_code == 200  
    assert response.json == [{"id": 1, "message": "Reminder 1"}]  
  
def test_reminder_post(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"status": "success", "message": "Reminder saved"}  
  
    response = client.post('/reminder', json={"message": "New Reminder"})  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "Reminder saved"}  
  
def test_history_get(client, mock_requests_get):  
    mock_requests_get.return_value.status_code = 200  
    mock_requests_get.return_value.json.return_value = [{"id": 1, "message": "History 1"}]  
  
    response = client.get('/history/1')  
    assert response.status_code == 200  
    assert response.json == [{"id": 1, "message": "History 1"}]  
  
def test_reminder_detail_get(client, mock_requests_get):  
    mock_requests_get.return_value.status_code = 200  
    mock_requests_get.return_value.json.return_value = {"id": 1, "message": "Reminder 1"}  
  
    response = client.get('/reminder/1')  
    assert response.status_code == 200  
    assert response.json == {"id": 1, "message": "Reminder 1"}  
  
def test_reminder_detail_put(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"status": "success", "message": "Reminder updated"}  
  
    response = client.put('/reminder/1', json={"message": "Updated Reminder"})  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "Reminder updated"}  
  
def test_reminder_detail_delete(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"status": "success", "message": "Reminder deleted"}  
  
    response = client.delete('/reminder/1')  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "Reminder deleted"}  
  
def test_send_message(client, mock_requests_post):  
    mock_requests_post.return_value.status_code = 200  
    mock_requests_post.return_value.json.return_value = {"status": "success", "message": "Message sent"}  
  
    response = client.post('/send_message', json={"token": "testtoken", "target": "testtarget", "message": "Hello"})  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "Message sent"}  
  
def test_send_notification(client):  
    response = client.post('/send_notification', json={"message": "Test Notification"})  
    assert response.status_code == 200  
    assert response.json == {"status": "success", "message": "Notification sent via WebSocket"}  
