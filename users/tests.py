from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_signup_successful(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'Password123!',
            'password-confirm': 'Password123!' # Django UserCreationForm password confirm field name can vary, let's check
        })
        # Wait, the field names for Password confirm in UserCreationForm are password1 and password2 usually.
        # But CustomUserCreationForm inherits from UserCreationForm.
        # Let's check UserCreationForm source or just use the typical password1/password2.
        
        # Actually, let's check the fields in CustomUserCreationForm.
        # Inherited from UserCreationForm (default): username, password1, password2.
        # Added: first_name, last_name, email.
        
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!'
        })
        self.assertEqual(response.status_code, 302) # Redirect to home
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_login_successful_with_email(self):
        User.objects.create_user(username='testuser2', email='test2@example.com', password='Password123!')
        response = self.client.post(self.login_url, {
            'username': 'test2@example.com',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(email='test2@example.com').pk)

    def test_login_unmatched_credentials(self):
        User.objects.create_user(username='testuser3', email='test3@example.com', password='Password123!')
        response = self.client.post(self.login_url, {
            'username': 'test3@example.com',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200) # Re-renders login page
        # Check for error message in context or content
        self.assertContains(response, "Unmatched email and password.")
