from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from api.models import Task

User = get_user_model()


def create_user():
    data = {
        'username': 'test_user',
        'password': 'test_password',
        'first_name': 'test',
        'last_name': 'user',
        'email': 'testuser@example.com',
    }
    user = User.objects.create_user(**data)
    return user


class AuthenticationTests(APITestCase):
    def test_user_registration_success(self):
        data = {
            'username': 'new_user',
            'password': 'Test$1234',
            'first_name': 'new',
            'last_name': 'user',
            'email': 'newuser@example.com',
        }
        response = self.client.post(reverse('register'), data, format='json')
        new_user = User.objects.get(username=data['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_failure_missing_fields(self):
        data = {'username': 'new_user'}
        response = self.client.post(reverse('register'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_failure_existing_username(self):
        user = create_user()
        data = {'username': user.username, 'password': 'new_password'}
        response = self.client.post(reverse('register'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_failure_weak_password(self):
        data = {'username': 'new_user', 'password': 'password'}
        response = self.client.post(reverse('register'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        user = create_user()
        credentials = {'username': user.username, 'password': 'test_password'}
        response = self.client.post(reverse('login'), data=credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure_wrong_credentials(self):
        user = create_user()
        credentials = {'username': user.username, 'password': 'wrong_password'}
        response = self.client.post(reverse('login'), data=credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_failure_missing_credentials(self):
        user = create_user()
        credentials = {'username': user.username}
        response = self.client.post(reverse('login'), data=credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskTests(APITestCase):
    def setUp(self):
        user = create_user()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.headers = {'Authorization': f'Bearer {access_token}'}

    def test_get_all_task(self):
        task1 = Task.objects.create(title="Task 1", description="New Task 1", completed=True)
        task2 = Task.objects.create(title="Task 2", description="New Task 2")

        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_single_task(self):
        task = Task.objects.create(title="Task Detail", description="New Task", completed=True)
        response = self.client.get(reverse('task_detail', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)
        self.assertEqual(response.data['description'], task.description)
        self.assertTrue(task.completed)

    def test_create_task_authenticated_user(self):
        data = {'title': 'New Task', 'description': 'This is a new task.'}
        response = self.client.post(reverse('task_list'), data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertFalse(response.data['completed'])

    def test_create_task_unauthenticated_user(self):
        data = {'title': 'New Task', 'description': 'This is a new task.'}
        response = self.client.post(reverse('task_list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_authenticated_user(self):
        task = Task.objects.create(title="New Task", description="Created New Task")
        data = {'title': 'Updated Task', 'description': 'Updated Task description'}
        response = self.client.put(reverse('task_detail', args=[task.id]), data, format='json', headers=self.headers)
        updated_task = Task.objects.get(id=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_task.title, data['title'])
        self.assertEqual(updated_task.description, data['description'])
        self.assertFalse(updated_task.completed)

    def test_update_task_unauthenticated_user(self):
        task = Task.objects.create(title="New Task", description="Created New Task")
        data = {'title': 'Updated Task', 'description': 'Updated Task description'}
        response = self.client.put(reverse('task_detail', args=[task.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_task_authenticated_user(self):
        task = Task.objects.create(title="New Task", description="Created New Task")
        response = self.client.delete(reverse('task_detail', args=[task.id]), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_unauthenticated_user(self):
        task = Task.objects.create(title="New Task", description="Created New Task")
        response = self.client.delete(reverse('task_detail', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
