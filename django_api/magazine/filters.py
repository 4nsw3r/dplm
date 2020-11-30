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
    updated_at = filters.DateFromToRangeFilter()

    status = filters.ChoiceFilter(choices=Orders.STATUSES)

    products = filters.ModelMultipleChoiceFilter(
        field_name='products__name',
        to_field_name='name',
        queryset=Product.objects.all()
    )

    class Meta:
        model = Orders
        fields = ('id', 'status', 'created_at', 'updated_at', 'products')


class ReviewFilter(filters.FilterSet):
    """Фильтры для отзывов."""

    id = filters.ModelMultipleChoiceFilter(
        field_name='id',
        to_field_name='id',
        queryset=ProductReviews.objects.all()
    )

    created_at = filters.DateFromToRangeFilter()

    review = filters.ModelMultipleChoiceFilter(
        field_name='review__id',
        to_field_name='id',
        queryset=Product.objects.all()
    )
    # creator = filters.ModelMultipleChoiceFilter(
    #     field_name='creator',
    #     to_field_name='creator__id',
    #     queryset=ProductReviews.objects.all()
    # )

    class Meta:
        model = ProductReviews
        fields = ('id', 'review', 'creator', 'created_at')