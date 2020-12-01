from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter, OrderFilter, ReviewFilter
from .models import Orders, Product, ProductReviews, Collections
from .serializers import OrderSerializer, ProductSerializer, ReviewsSerializer, CollectionsSerializer
from .permissions import isAllowed


class OrdersViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = Orders.objects.prefetch_related("positions").all()
        user = self.request.user
        queryset_id = Orders.objects.filter(creator=user)
        if user.is_superuser:
            return queryset
        else:
            return queryset_id

    permission_classes_by_action = {'list': [IsAuthenticated],
                                    'retrieve': [isAllowed],
                                    'create': [IsAuthenticated],
                                    'destroy': [isAllowed],
                                    'update': [IsAdminUser],
                                    'partial_update': [IsAdminUser]
                                    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    permission_classes_by_action = {'list': [AllowAny],
                                    'retrieve': [AllowAny],
                                    'create': [IsAdminUser],
                                    'destroy': [IsAdminUser],
                                    'update': [IsAdminUser],
                                    'partial_update': [IsAdminUser]
                                    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class ReviewsViewSet(ModelViewSet):
    queryset = ProductReviews.objects.select_related('review').all()
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset = ReviewFilter

    permission_classes_by_action = {'list': [AllowAny],
                                    'retrieve': [AllowAny],
                                    'create': [IsAuthenticated],
                                    'destroy': [isAllowed],
                                    'update': [isAllowed],
                                    'partial_update': [isAllowed]
                                    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class CollectionsViewSet(ModelViewSet):
    queryset = Collections.objects.prefetch_related("products").all()
    serializer_class = CollectionsSerializer
    #    permission_classes = [IsAdminUser]

    permission_classes_by_action = {'list': [AllowAny],
                                    'retrieve': [AllowAny],
                                    'create': [IsAdminUser],
                                    'destroy': [IsAdminUser],
                                    'update': [IsAdminUser],
                                    'partial_update': [IsAdminUser]
                                    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
