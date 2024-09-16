# tests/test_app.py

def test_login_page(client):
    response = client.post('/auth/login', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
