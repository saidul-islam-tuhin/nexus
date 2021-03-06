# Standard Library
import json

# Third Party Stuff
import pytest
from django.urls import reverse

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_get_current_user_api(client):
    url = reverse('me')
    user = f.create_user(email='test@example.com')

    # should require auth
    response = client.get(url)
    assert response.status_code == 401

    client.login(user)
    response = client.get(url)

    # assert response is None
    assert response.status_code == 200
    expected_keys = [
        'id', 'first_name', 'last_name', 'email', 'gender', 'tshirt_size', 'ticket_id', 'phone_number',
        'is_core_organizer', 'is_volunteer', 'date_joined', 'is_active', 'is_staff', 'is_superuser'
    ]
    assert set(expected_keys).issubset(response.data.keys())
    assert response.data['id'] == str(user.id)


def test_patch_current_user_api(client):
    url = reverse('me')
    user = f.create_user(email='test@example.com', first_name='test', last_name='test')

    # user can update only the following fields
    data = {
        'first_name': 'modified_test',
        'last_name': 'modified_test',
        'email': 'modified_test@example.com',
        'gender': 'male',
        'tshirt_size': 'extra_extra_large',
        'phone_number': '+912233445566'
    }

    # should require auth
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 401

    client.login(user)
    response = client.json.patch(url, json.dumps(data))
    # assert response is None
    assert response.status_code == 200
    expected_keys = [
        'id', 'first_name', 'last_name', 'email', 'gender', 'tshirt_size', 'ticket_id', 'phone_number',
        'is_core_organizer', 'is_volunteer', 'date_joined', 'is_active', 'is_staff', 'is_superuser'
    ]
    assert set(expected_keys).issubset(response.data.keys())

    assert response.data['first_name'] == data['first_name']
    assert response.data['last_name'] == data['last_name']
    assert response.data['email'] == data['email']
    assert response.data['gender'] == data['gender']
    assert response.data['tshirt_size'] == data['tshirt_size']
    assert response.data['phone_number'] == data['phone_number']
