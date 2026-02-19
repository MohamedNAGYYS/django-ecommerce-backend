from django.test import TestCase
from .models import Users


class UserTest(TestCase):
    def test_create_user(self):
        # I create a normal user
        user = Users.objects.create_user(
            first_name='Mohamed',
            last_name='Nagy',
            email='mohamed@gmail.com',
            password='mohamedpass123'
        )

        self.assertEqual(user.email, 'mohamed@gmail.com') # Test if user.email == mohamed@gmail.com
        self.assertTrue(user.check_password('mohamedpass123')) # Test if password is hashed already
        self.assertFalse(user.is_staff) # Test if user.is_staff = False
        self.assertEqual(user.role, Users.RoleChocies.CUSTOMER) # Test if user.role = Users.RoleChocies.CUSTOMER


    def test_create_superuser(self):
        # I create an admin to test
        user = Users.objects.create_superuser(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password='admin123'
        )

        self.assertTrue(user.is_staff) # Test if user.is_staff = True
        self.assertTrue(user.is_superuser) # Test if user.superuser = True
        self.assertEqual(user.role, Users.RoleChocies.ADMIN) # Check if the role in user = the role in RoleChoices
    
    def test_str_returns_email(self):
        user = Users.objects.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='pass123'
        )
        # Check if __str__ method return the email
        self.assertEqual(str(user), 'test@example.com')

        # I check any email duplicates
        users = Users.objects.all()
        emails = [u.email for u in users]
        self.assertIn(user.email, emails)   