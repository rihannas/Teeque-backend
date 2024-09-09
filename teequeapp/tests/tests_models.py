from django.test import TestCase
from django.contrib.auth.hashers import check_password
from ..models import *

# Create your tests here.

class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        superuser = CustomUser.objects.create_superuser(email='admin@email.com', username='admin', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')

    def setUp(self):
        self.user = CustomUser.objects.get(pk=1)
        self.superuser = CustomUser.objects.get(username='admin')


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

    # super user tests
    def test_create_superusr(self):
        self.assertEqual(self.superuser.username, 'admin')

        
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

class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='writing')     
    def setUp(self):
        self.category = Category.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.category.__str__(), 'writing')

class TestOrderModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        buyer = Buyer(user=user)
        buyer.save()

        user = CustomUser.objects.create_user(email='moon@email.com', username='moon', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        seller = Seller(user=user)
        seller.save()  

        category = Category.objects.create(name='writing')   

        service = Service.objects.create(
            title='Sample Service',
            category=category,
            description='This is a sample service description.',
            price=Decimal('99.99'),
            seller=seller
        )

        order = Order.objects.create(buyer=buyer)   

    def setUp(self):
        self.order = Order.objects.get(pk=1)
        self.buyer = Buyer.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.order.__str__(),  f"List Order #1 of {self.buyer.user.username}")


class TestOrderItemModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        buyer = Buyer(user=user)
        buyer.save()

        user = CustomUser.objects.create_user(email='moon@email.com', username='moon', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        seller = Seller(user=user)
        seller.save()  

        category = Category.objects.create(name='writing')   

        service = Service.objects.create(
            title='Sample Service',
            category=category,
            description='This is a sample service description.',
            price=Decimal('99.99'),
            seller=seller
        )

        order = Order.objects.create(buyer=buyer)

        orderItem = OrderItem.objects.create(service=service, order=order)

    def setUp(self):
        self.orderItem = OrderItem.objects.get(pk=1)
        self.service = Service.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.orderItem.__str__(),  f"{self.service}")



class TestTagModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        tag = Tag.objects.create(tag='webdev')     
    def setUp(self):
        self.tag = Tag.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.tag.__str__(), 'webdev')

class TesRatingModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='sun@email.com', username='sun', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        buyer = Buyer(user=user)
        buyer.save()

        user = CustomUser.objects.create_user(email='moon@email.com', username='moon', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        seller = Seller(user=user)
        seller.save()  

        category = Category.objects.create(name='writing')   

        service = Service.objects.create(
            title='Sample Service',
            category=category,
            description='This is a sample service description.',
            price=Decimal('99.99'),
            seller=seller
        )

        rating = Rating.objects.create(buyer=buyer, service=service, rating=3, comment='blah blah')   

    def setUp(self):
        self.service = Service.objects.get(pk=1)
        self.buyer = Buyer.objects.get(pk=1)
        self.rating = Rating.objects.get(pk=1)
    
    def test_str_method(self):
        self.assertEqual(self.rating.__str__(),  f"Rating for {self.service.title} by {self.buyer.user.username}" )

