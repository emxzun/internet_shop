from django.contrib.auth import get_user_model
from django.db import models

from applications.product.models import Product

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    order_confirm = models.BooleanField(default=False)
    code = models.CharField(max_length=100, blank=True)

    def create_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.code = code
