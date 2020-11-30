from django.conf import settings
from django.db import models


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

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'


class ProductReviews(TimestampFields):
    """Отзыв к товару"""
    review = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews', verbose_name="Товар")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    text = models.TextField(max_length=1000, verbose_name="Отзыв")
    mark = models.PositiveIntegerField(verbose_name="Оценка")

    class Meta:
        verbose_name_plural = 'Reviews'
        verbose_name = 'Review'


class ProductOrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товары")
    order = models.ForeignKey("Orders", related_name='positions', on_delete=models.CASCADE, verbose_name="Заказ")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def get_cost(self):
        return self.product.price * self.quantity


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
        verbose_name="Пользователь"
    )
    status = models.CharField(max_length=12, choices=STATUSES, default="New", verbose_name="Статус")
    products = models.ManyToManyField(Product, through=ProductOrderPosition, verbose_name="Товары")

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.positions.all())

    order_sum = property(get_total_cost)

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'
        ordering = ['-created_at']

class Collections(TimestampFields):
    """Коллекции"""

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.TextField(max_length=1000, verbose_name="Описание")
    products = models.ManyToManyField(Product, verbose_name="Товары")

    class Meta:
        verbose_name_plural = 'Collections'
        verbose_name = 'Collection'

    def __str__(self):
        return self.title
