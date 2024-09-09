from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from teequeapp.models import *

class ServiceTests(APITestCase):

    def test_view_services(self):
        url = reverse('teequeapi:services-list')
        reponse = self.client.get(url, format='json')

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


        self.assertEqual(reponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Seller.objects.count(), 1)