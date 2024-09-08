from django.test import TestCase
from django.contrib.auth.hashers import check_password
from ..models import *

# Create your tests here.

class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        
    def setUp(self):
        self.user = CustomUser.objects.get(pk=1)

    def test_user_created(self):
        self.assertEqual(self.user.id, 1)

    def test_user_password_hashed(self):
        password = 'ilovedjango'
        self.assertNotEqual(self.user.password, password)
        self.assertTrue(self.user.password.startswith('pbkdf2_sha256$'))
        self.assertTrue(check_password(password, self.user.password))

    
    def test_email_is_unique(self):
        with self.assertRaises(ValueError): 
            user2 = CustomUser.objects.create_user(email='sun@email.com', username='moon', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        

        

