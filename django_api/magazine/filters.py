from django_filters import rest_framework as filters

from .models import Product, Orders, ProductReviews


class ProductFilter(filters.FilterSet):
    """Фильтры для продуктов."""

    id = filters.ModelMultipleChoiceFilter(
        field_name='id',
        to_field_name='id',
        queryset=Product.objects.all()
    )
    name = filters.CharFilter(lookup_expr='iexact')
    desc = filters.CharFilter(lookup_expr='iexact')
    price_from = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('name', 'desc', 'price')


class OrderFilter(filters.FilterSet):
    """Фильтры для заказов."""

    id = filters.ModelMultipleChoiceFilter(
        field_name='id',
        to_field_name='id',
        queryset=Orders.objects.all()
    )

    created_at = filters.DateFromToRangeFilter()
    update_at = filters.DateFromToRangeFilter()

    status = filters.ChoiceFilter(choices=Orders.STATUSES)

    products = filters.ModelMultipleChoiceFilter(
        field_name='products__name',
        to_field_name='name',
        queryset=Product.objects.all()
    )

    class Meta:
        model = Orders
        fields = ('id', 'status', 'created_at', 'update_at', 'products')