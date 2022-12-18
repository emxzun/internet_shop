

from rest_framework import serializers

from applications.order.models import Order
from applications.product.models import Product
from applications.order.tasks import send_confirmation_link


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        exclude = ['code', 'order_confirm']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.create_code()
        order.save()
        send_confirmation_link.delay(order.user.email, order.code)
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        product = Product.objects.get(id=rep['product']).title
        rep['order_confirm'] = instance.order_confirm
        rep['product'] = product
        return rep

