from django.conf import settings
from django.db import models
#from django.contrib.auth.models import User


class TimestampFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Product(TimestampFields):
    """Товар"""

    name = models.CharField(max_length=100, verbose_name="Название")
    desc = models.TextField(default="description for product", verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name


class ProductReviews(TimestampFields):
    """Отзыв к товару"""
    review = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    text = models.TextField(max_length=1000)
    mark = models.PositiveIntegerField()


class ProductOrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey("Orders", related_name='positions', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # def save(self, *args, **kwargs):
    #     prod = ProductOrderPosition.objects.all()
    #     total = 0.00
    #     total = math.fsum(item.quantity * item.product.price for item in prod)
    #     self.order.order_sum = total
    #     super(ProductOrderPosition, self).save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     price = self.product.price
    #     items = self.quantity
    #     total = price * items
    #     self.order.order_sum = total
    #     super(ProductOrderPosition, self).save(*args, **kwargs)


class Orders(TimestampFields):
    """Заказы"""

    STATUSES = (
        ("New", "Новый"),
        ("In_progress", "Выполняется"),
        ("Done", "Готов"),
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=12, choices=STATUSES, default="New")
    order_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products = models.ManyToManyField(Product, through=ProductOrderPosition)

        
        
# class Collections(TimestampFields):
#     """Коллекции"""
#
#     title = models.CharField(max_length=100)
#     text = models.TextField(max_length=1000)
#     products = models.ForeignKey
