from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from teequeapp.models import *

class ServiceViewSetTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='moon@email.com', username='moon', password='ilovedjango', about='ilovesun', phonenumber='+12345678900')
        self.seller = Seller(user=self.user)
        self.seller.save()  

        self.category = Category.objects.create(name='writing')   

        self.service = Service.objects.create(
            title='Sample Service',
            category=self.category,
            description='This is a sample service description.',
            price=Decimal('99.99'),
            seller=self.seller
        )


    def test_view_services(self):
        url = reverse('teequeapi:services-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_service(self):
        url = reverse('teequeapi:services-detail', kwargs={'pk': self.service.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Service')