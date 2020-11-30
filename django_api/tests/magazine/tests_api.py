import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED, HTTP_201_CREATED

from magazine.models import Product
#from django_api.magazine.models import Product, ProductReviews, Orders, Collections

headers_admin = {'Authorization': 'Token 29e07421a0aa6d49dc35a6c5c05aa2b3891d2079'}
headers_user = {'Authorization': 'Token 5d0a3e97adb8d302f9366c9dd962c774bfbfd944'}


@pytest.mark.django_db
def test_product_get(api_client):
    url = reverse('products-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
