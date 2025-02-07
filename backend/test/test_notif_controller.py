import pytest  
from unittest.mock import patch  
from app.controller.NotifController import send_message, send_notif, send_notification_via_websocket  
  
# Uji fungsi send_message  
@patch('app.controller.NotifController.requests.post')  
def test_send_message_success(mock_post):  
    # Siapkan mock response  
    mock_post.return_value.status_code = 200  
    mock_post.return_value.json.return_value = {"success": True}  
  
    response = send_message("test_token", "test_target", "Hello, World!")  
      
    assert response == {"success": True}  
    mock_post.assert_called_once()  
  
@patch('app.controller.NotifController.requests.post')  
def test_send_message_failure(mock_post):  
    # Siapkan mock response untuk kegagalan  
    mock_post.side_effect = Exception("Network error")  
  
    response = send_message("test_token", "test_target", "Hello, World!")  
      
    assert response == {"error": "Network error"}  
    mock_post.assert_called_once()  
  
# Uji fungsi send_notif  
@patch('app.controller.NotifController.emit')  
def test_send_notif_success(mock_emit):  
    response = send_notif("test_token", "test_target", "Hello, Notification!")  
      
    assert response is None  # Fungsi ini tidak mengembalikan nilai  
    mock_emit.assert_called_once_with("notification", "Hello, Notification!")  
  
# Uji fungsi send_notification_via_websocket  
@patch('app.controller.NotifController.socketio.emit')  
def test_send_notification_via_websocket(mock_emit):  
    message = "WebSocket Notification"  
    send_notification_via_websocket(message)  
      
    mock_emit.assert_called_once_with('notification', {'message': message}, broadcast=True)  
