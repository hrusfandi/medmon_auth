from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:user_list')
OBTAIN_TOKEN_URL = reverse('user:token_obtain')
REFRESH_TOKEN_URL = reverse('user:token_refresh')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test that JWT toke is created for user"""
        payload = {'email': 'test@qdstudio.com', 'password': 'password123'}
        create_user(**payload)

        res = self.client.post(OBTAIN_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_refresh_token_for_user(self):
        """Test that JWT token can be refreshed using refresh token."""
        payload = {'email': 'test@qdstudio.com', 'password': 'password123'}
        create_user(**payload)

        res = self.client.post(OBTAIN_TOKEN_URL, payload)
        payload = {'refresh': res.data['refresh']}
        res_refresh = self.client.post(REFRESH_TOKEN_URL, payload)

        self.assertEqual(res_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('access', res_refresh.data)


class PrivateUserAPITests(TestCase):
    """Test the user API (private)"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='admin@qdstudio.com',
            password='password123',
            name='User Admin'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@qdstudio.com',
            'password': 'password123',
            'name': 'User Test'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        res.data.pop('groups')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'test@qdstudio.com',
            'password': 'password123',
            'name': 'User Test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than equal 5 chars"""
        payload = {
            'email': 'test@qdstudio.com',
            'password': 'pwd',
            'name': 'User Test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
