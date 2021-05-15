from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from tasks.serializers import TaskSerializer
from tasks.models import Task

import json 

class ModelTestCase(TestCase):
    def testModel(self):
        task = Task(name="My Task", description="Test Case")
        self.assertEqual(task.name, "My Task")
        self.assertEqual(task.description, "Test Case")
        self.assertTrue(task.date)

class TaskViewSetTestCase(APITestCase):
    
    def setUp(self):
        self.base_data = {
            'name' : 'task #1'
        }

        self.url_name = 'tasks'

    def create_task(self):
        serializer = TaskSerializer(data=self.base_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def test_task_create(self):
        response = self.client.post(reverse(self.url_name),json.dumps(self.base_data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.base_data['name'])
        self.assertTrue(response.data['date'])

    def test_task_detail(self):
        self.create_task()
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        

    def test_task_partial_update(self):
        data = self.create_task()
        to_update = {
            'description' : 'desc for #1'
        }
        data.update(to_update)
        
        response = self.client.patch(reverse(self.url_name, kwargs={'pk':data['id']}), json.dumps(to_update), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['description'], to_update['description'])
        
        self.assertEqual(response.data, data)