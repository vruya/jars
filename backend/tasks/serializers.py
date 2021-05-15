from rest_framework import serializers
from .models import Task

class DateTimeRelatedField(serializers.DateTimeField):
    def to_representation(self, instance):
        return instance.strftime("%Y-%m-%d %H:%M") if instance else None

class TaskSerializer(serializers.ModelSerializer):
    date = DateTimeRelatedField(required=False)

    class Meta:
        model = Task
        fields = '__all__'
