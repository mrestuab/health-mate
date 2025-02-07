import pytest  
from unittest.mock import patch, MagicMock  
from app import app, db  
from app.controller.ReminderController import show, detail, save, ubah, hapus  
  
@pytest.fixture  
def client():  
    app.config['TESTING'] = True  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Menggunakan database in-memory untuk pengujian  
    with app.test_client() as client:  
        with app.app_context():  
            db.create_all()  # Membuat semua tabel  
        yield client  
        with app.app_context():  
            db.drop_all()  # Menghapus semua tabel setelah pengujian  
  
def test_show(client):  
    # Simulasi data yang ada di database  
    # Anda bisa menambahkan data ke database di sini jika perlu  
    response = client.get('/reminder?user_id=1')  
    assert response.status_code == 200  
    assert 'Sukses Mengambil Data' in response.get_data(as_text=True)  
  
def test_detail(client):  
    # Simulasi data yang ada di database  
    response = client.get('/reminder/1')  # Ganti dengan ID yang sesuai  
    assert response.status_code == 200  
    assert 'Sukses Mengambil Detail Data' in response.get_data(as_text=True)  
  
def test_save(client):  
    # Simulasi data yang akan disimpan  
    data = {  
        'reminder_time': '2025-01-19 10:00:00',  
        'description': 'Test Reminder',  
        'frequency': 1,  
        'user_id': 1,  
        'medicine_name': 'Paracetamol',  
        'dosage': '500mg',  
        'start_date': '2025-01-19',  
        'end_date': '2025-01-20'  
    }  
    response = client.post('/reminder', json=data)  
    assert response.status_code == 200  
    assert 'Sukses Menambahkan Data Reminder dan Medicine' in response.get_data(as_text=True)  
  
def test_ubah(client):  
    # Simulasi data yang akan diubah  
    data = {  
        'reminder_time': '2025-01-19 11:00:00',  
        'description': 'Updated Reminder',  
        'frequency': 2,  
        'medicine_name': 'Ibuprofen',  
        'dosage': '400mg'  
    }  
    response = client.put('/reminder/1', json=data)  # Ganti dengan ID yang sesuai  
    assert response.status_code == 200  
    assert 'Sukses Mengupdate Data Reminder dan Medicine' in response.get_data(as_text=True)  
  
def test_hapus(client):  
    # Simulasi penghapusan  
    response = client.delete('/reminder/1')  # Ganti dengan ID yang sesuai  
    assert response.status_code == 200  
    assert 'Sukses Menghapus Data Reminder dan Medicine' in response.get_data(as_text=True)  
