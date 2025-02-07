import pytest  
from unittest.mock import patch, MagicMock  
from app import app, db  
from flask_jwt_extended import create_access_token  
from app.model.user import User  
  
@pytest.fixture  
def client():  
    with app.test_client() as client:  
        with app.app_context():  
            db.create_all()  # Buat database in-memory  
        yield client  
        with app.app_context():  
            db.drop_all()  # Hapus database setelah pengujian  
  
def test_login_success(client):  
    # Setup  
    user = User(name="Test User", email="test@example.com", phone_number="1234567890")  
    user.setPassword("password")  
    db.session.add(user)  
    db.session.commit()  
  
    # Test  
    response = client.post('/login', json={"email": "test@example.com", "password": "password"})  
    data = response.get_json()  
  
    assert response.status_code == 200  
    assert "access_token" in data  
    assert "refresh_token" in data  
  
def test_login_invalid_email(client):  
    response = client.post('/login', json={"email": "invalid@example.com", "password": "password"})  
    data = response.get_json()  
  
    assert response.status_code == 400  
    assert data['message'] == "Email tidak terdaftar"  
  
def test_login_invalid_password(client):  
    user = User(name="Test User", email="test@example.com", phone_number="1234567890")  
    user.setPassword("password")  
    db.session.add(user)  
    db.session.commit()  
  
    response = client.post('/login', json={"email": "test@example.com", "password": "wrongpassword"})  
    data = response.get_json()  
  
    assert response.status_code == 400  
    assert data['message'] == "Kombinasi email dan password salah"  
  
def test_register_user_success(client):  
    response = client.post('/register', json={  
        "name": "New User",  
        "email": "newuser@example.com",  
        "phone_number": "0987654321",  
        "password": "password"  
    })  
    data = response.get_json()  
  
    assert response.status_code == 200  
    assert data['message'] == "User berhasil didaftarkan!"  
  
def test_register_user_existing_email(client):  
    user = User(name="Existing User", email="existing@example.com", phone_number="1234567890")  
    user.setPassword("password")  
    db.session.add(user)  
    db.session.commit()  
  
    response = client.post('/register', json={  
        "name": "New User",  
        "email": "existing@example.com",  
        "phone_number": "0987654321",  
        "password": "password"  
    })  
    data = response.get_json()  
  
    assert response.status_code == 400  
    assert data['message'] == "Email sudah digunakan!"  
  
def test_get_user_profile(client):  
    user = User(name="Test User", email="test@example.com", phone_number="1234567890")  
    user.setPassword("password")  
    db.session.add(user)  
    db.session.commit()  
  
    access_token = create_access_token(identity={"user_id": user.user_id})  
  
    response = client.get('/profile', headers={"Authorization": f"Bearer {access_token}"})  
    data = response.get_json()  
  
    assert response.status_code == 200  
    assert data['data']['email'] == "test@example.com"  
  
def test_get_all_users(client):  
    user1 = User(name="User One", email="user1@example.com", phone_number="1234567890")  
    user1.setPassword("password")  
    user2 = User(name="User Two", email="user2@example.com", phone_number="0987654321")  
    user2.setPassword("password")  
    db.session.add(user1)  
    db.session.add(user2)  
    db.session.commit()  
  
    response = client.get('/users')  
    data = response.get_json()  
  
    assert response.status_code == 200  
    assert len(data['data']) == 2  
