from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"Статус заказа - {self.name}"

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=0)
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=20, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=130, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"Заказ - {self.id}, статус - {self.status.name}"

    class Meta:
        verbose_name = 'Заказ'  # то как в джанго админке будет называться 1 модель в меню приложения
        verbose_name_plural = 'Заказы'  # то как будет называться множество моедлей в приложении


class ProductInOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True, default=None)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"Товар - {self.product.name}"

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        self.price_per_one = self.product.price
        total_price = int(self.nmb) * self.price_per_one
        self.total_price = total_price
        order = self.order
        all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
        order_total_price = 0
        for item in all_products_in_order:
            order_total_price += item.total_price
        order.total_price = order_total_price + total_price
        order.save(force_update=True)
        super().save(*args, **kwargs)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True, default=None)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * self.price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)
