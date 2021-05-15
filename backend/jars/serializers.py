from rest_framework import serializers, exceptions
from .models import Jar, Operation
from django.shortcuts import get_object_or_404
from django.db import transaction

from decimal import Decimal
import datetime
import operator

class JarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jar
        fields = '__all__'

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

    def raise_operation(self, obj):
        obj.status = 'failed'
        obj.save()

    def valdiate(self, data):
        try:
            data['amount'] = Decimal(data['amount'])
        except:
            raise exceptions.NotAcceptable('Amount is not valid!')

        return data

    def create(self, validated_data):
        request = self.context.get("request")
      
        try:
            date_start = request.data['date_start']
        except KeyError:
            raise exceptions.NotAcceptable('Date start not provided!')

        a,b=date_start, datetime.datetime.now()

        validated_data['duration'] = (datetime.datetime.now() - date_start).total_seconds()

        operation = super(OperationSerializer, self).create(validated_data)
        jar = operation.jar
        if jar.currency != operation.currency:
            self.raise_operation(operation)
            print('Currency do not match with jar!')
            return operation

        if operation.amount > jar.amount:
            self.raise_operation(operation)
            print('Insufficient funds in the jar!')
            return operation

        with transaction.atomic():
            oper = getattr(operator, validated_data['type'])
            jar.amount = oper(jar.amount, operation.amount)
            jar.save()

        return operation
            