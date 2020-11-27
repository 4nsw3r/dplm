from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter, OrderFilter
from .models import Orders, Product, ProductReviews
from .serializers import OrderSerializer, ProductSerializer, ReviewsSerializer


class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.prefetch_related("positions").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter



class ReviewsViewSet(ModelViewSet):
    queryset = ProductReviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]