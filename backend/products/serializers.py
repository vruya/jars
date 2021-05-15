from rest_framework import serializers
from .models import Product, Category, Order, OrderItem


class DateTimeRelatedField(serializers.DateTimeField):
    def to_representation(self, instance):
        return instance.strftime("%Y-%m-%d %H:%M") if instance else None

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    ordered_at = DateTimeRelatedField(required=False)

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

