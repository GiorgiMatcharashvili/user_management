# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class UserRegistrationTests(TestCase):
    def test_user_registration(self):
        client = APIClient()
        data = {
            'username': 'test',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }
        response = client.post(reverse('user-registration'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_user_authentication(self):
        client = APIClient()
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = client.post(reverse('user-authentication'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)
        self.assertEqual(response.data['message'], 'Authentication successful')


class UserDetailsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_get_user_details(self):
        client = APIClient()
        response = client.get(reverse('user-details', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in response.data)
        self.assertEqual(response.data['id'], self.user.id)

    def test_update_user_details(self):
        client = APIClient()
        data = {
            'username': self.user.username,
            'password': self.user.password,
            'first_name': 'UpdatedName'
        }
        response = client.put(reverse('user-details', args=[self.user.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'UpdatedName')

    def test_delete_user(self):
        client = APIClient()
        response = client.delete(reverse('user-details', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class UserPermissionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_assign_permissions(self):
        client = APIClient()
        data = {
            'permission': 'add_user'
        }
        response = client.post(reverse('user-permissions', args=[self.user.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)
        self.assertEqual(response.data['message'], 'Permission add_user assigned successfully')
