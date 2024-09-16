# tests/test_auth.py

def test_signup(client):
    response = client.post('/auth/signup', json={
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'password123',
        'confirmPassword': 'password123'
    })
    assert response.status_code == 200
