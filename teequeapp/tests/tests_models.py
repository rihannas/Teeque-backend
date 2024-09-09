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
    
    # test the phone number doesn't exist
    # test the phone number wrong

    def test_user_phonenumber_exists(self):
        phonenumber = '+12345678900'
        self.assertEqual(self.user.phonenumber, phonenumber)

    # check the country has the right digits
    
    def test_user_phonenumber_type(self):
        phonenumber = '12345678900'

        #AssertionError: PhoneNumber(country_code=1, national_numb[143 chars]None) != 12345678900

        with self.assertRaises(AssertionError):
            self.assertEqual(self.user.phonenumber, phonenumber)

    def test_user_wrong_phonenumber(self):
        user2 = CustomUser.objects.create_user(email='moon@email.com', username='moon', password='ilovedjango', about='ilovesun', phonenumber='+1234567890')
        user = CustomUser.objects.get(pk=1)


        # self.assertEqual(user.phonenumber, user2.phonenumber)




    # test the country

    # Tests that last_login is automatically set




        
    # TODO: FIX THIS BECAUSE This is returning the wrong message
    # def test_username_is_unique(self):
    # # with self.assertRaises(ValueError): 
    # user2 = CustomUser.objects.create_user(email='moon@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        

class TestSellerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        seller = Seller(user=user)
        seller.save()       
    def setUp(self):
        self.seller = Seller.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.seller.__str__(), 'sun')

    def test_seller_is_saved_to_seller_group(self):
        seller_group = Group.objects.get(name='Seller') 
        self.assertEqual(self.seller.user.groups.get(name='Seller'), seller_group)

class TestSellerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        seller = Seller(user=user)
        seller.save()       
    def setUp(self):
        self.seller = Seller.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.seller.__str__(), 'sun')

    def test_seller_is_saved_to_seller_group(self):
        seller_group = Group.objects.get(name='Seller') 
        self.assertEqual(self.seller.user.groups.get(name='Seller'), seller_group)

class TestSellerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        seller = Seller(user=user)
        seller.save()       
    def setUp(self):
        self.seller = Seller.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.seller.__str__(), 'sun')

    def test_seller_is_saved_to_seller_group(self):
        seller_group = Group.objects.get(name='Seller') 
        self.assertEqual(self.seller.user.groups.get(name='Seller'), seller_group)

class TestBuyerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        buyer = Buyer(user=user)
        buyer.save()       
    def setUp(self):
        self.buyer = Buyer.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.buyer.__str__(), 'sun')

    def test_buyer_is_saved_to_buyer_group(self):
        buyer_group = Group.objects.get(name='Buyer') 
        self.assertEqual(self.buyer.user.groups.get(name='Buyer'), buyer_group)
