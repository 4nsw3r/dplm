from rest_framework.routers import SimpleRouter
from .views import OrdersViewSet, ProductViewSet, ReviewsViewSet, CollectionsViewSet

router = SimpleRouter()
router.register('orders', OrdersViewSet, basename='orders')
router.register('products', ProductViewSet, basename='products')
router.register('reviews', ReviewsViewSet, basename='reviews')
router.register('collections', CollectionsViewSet, basename='collections')
urlpatterns = router.urls
