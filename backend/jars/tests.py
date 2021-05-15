from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .serializers import JarSerializer
from .models import Jar

from decimal import Decimal
import json 

class JarViewSetTestCase(APITestCase):
    
    def setUp(self):
        self.base_data = {
            'name' : 'jar #1',
            'amount': 100,
            'currency': 'USD'
        }

        self.url_name = 'jars'

    def create_jar(self):
        serializer = JarSerializer(data=self.base_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def test_jar_create(self):
        response = self.client.post(reverse(self.url_name),json.dumps(self.base_data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.base_data['name'])
        self.assertTrue(response.data['added_at'])
   

    def test_operation_ok(self):
        jar = self.create_jar()
        data = {
            'title': "Everything is ok",
            'jar': jar['id'],
            'amount': 50,
            'type' : 'sub',
            'currency': 'USD',
        }
        amount_bef = jar['amount']
        response = self.client.post(reverse('operations'),json.dumps(data),content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        jar_after_oper = Jar.objects.get(id=jar['id'])
        self.assertEqual(Decimal(jar_after_oper.amount), Decimal(amount_bef)-Decimal(response.data['amount']))

    def test_operation_not_ok_curr(self):
        jar = self.create_jar()
        data = {
            'title': "Wrong currency",
            'jar': jar['id'],
            'amount': 50,
            'type' : 'sub',
            'currency': 'PLN',
        }
        amount_bef = jar['amount']
        response = self.client.post(reverse('operations'),json.dumps(data),content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'failed')
        jar_after_oper = Jar.objects.get(id=jar['id'])
        self.assertEqual(Decimal(jar_after_oper.amount), Decimal(amount_bef))

    def test_operation_not_ok_amount(self):
        jar = self.create_jar()
        data = {
            'title': "Not enough amount",
            'jar': jar['id'],
            'amount': 101,
            'type' : 'sub',
            'currency': 'USD',
        }   
        amount_bef = jar['amount']
        response = self.client.post(reverse('operations'),json.dumps(data),content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'failed')
        jar_after_oper = Jar.objects.get(id=jar['id'])
        self.assertEqual(Decimal(jar_after_oper.amount), Decimal(amount_bef))

        def test_operation_transfer(self):
            jar1 = self.create_jar()
            jar2 = self.create_jar()
            data1 = {
                'title': "transfer sub jar 1",
                'jar': jar1['id'],
                'amount': 50,
                'type' : 'sub',
                'currency': 'USD',
            } 

            data2 = {
                'title': "transfer add jar 2",
                'jar': jar2['id'],
                'amount': 50,
                'type' : 'sub',
                'currency': 'USD',
            }     

            response1 = self.client.post(reverse('operations'),json.dumps(data1),content_type='application/json')
            response2 = self.client.post(reverse('operations'),json.dumps(data2),content_type='application/json')

            self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response1.data['status'], 'success')
            self.assertEqual(response2.data['status'], 'success')
            jar_after_oper_1 = Jar.objects.get(id=jar1['id'])
            jar_after_oper_2 = Jar.objects.get(id=jar2['id'])
            self.assertEqual(Decimal(jar_after_oper_1.amount), 100-50)
            self.assertEqual(Decimal(jar_after_oper_2.amount), 100+50)


    def test_operation_get_filter(self):
        response = self.client.get(reverse('operations')+'?status=failed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('operations')+'?jar=2')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # does not exist!
        response = self.client.get(reverse('operations')+'?ordering=duration')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('operations')+'?ordering=amount')
        self.assertEqual(response.status_code, status.HTTP_200_OK)