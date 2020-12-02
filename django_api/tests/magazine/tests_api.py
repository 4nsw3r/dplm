import pytest

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, \
    HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_201_CREATED

from magazine.models import Product, ProductReviews, Orders, Collections


# тест на получение всех товаров
@pytest.mark.django_db
def test_product_list(api_client):
    url = reverse('products-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


# # тест на создание товаров в базе данных
# @pytest.mark.django_db
# def test_product_create(api_client):
#     product = Product.objects.bulk_create([
#         Product(name='Test_product_1', price=1000),
#         Product(name='Test_product_2', price=2000),
#         ])
#     url = reverse('products-list')
#     resp = api_client.get(url)
#
#     assert resp.status_code == HTTP_200_OK
#     resp_json = resp.json()
#     assert len(resp_json) == 2
#     assert resp_json[0]['name'] == product[0].name


# тест на создание товара без авторизации
@pytest.mark.django_db
def test_product_post(api_client):

    url = reverse('products-list')
    product_payload = {
        'name': 'Test_product',
        'desc': 'desc for test_product',
        'price': 100,
    }
    resp = api_client.post(url, product_payload)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


# тест на создание товара с авторизацией админа
@pytest.mark.django_db
def test_product_post_admin(api_admin):

    url = reverse('products-list')
    product_payload = {
        'name': 'Test_product',
        'desc': 'desc for test_product',
        'price': 100,
    }

    resp = api_admin.post(url, product_payload)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json['name'] == product_payload.get('name')


# тест на создание товара с авторизацией юзера
@pytest.mark.django_db
def test_product_post_user(api_user):

    url = reverse('products-list')
    product_payload = {
        'name': 'Test_product',
        'desc': 'desc for test_product',
        'price': 100,
    }

    resp = api_user.post(url, product_payload)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест на изменение товара с авторизацией админа
@pytest.mark.django_db
def test_product_update_admin(api_admin, product_factory):

    product = product_factory()
    params = {'name': 'Test_product'}
    url = reverse('products-detail', args=(product.id,))
    resp = api_admin.patch(url, params)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['id'] == product.id
    assert resp_json['name'] == params.get('name')


# тест на изменение товара с авторизацией юзера
@pytest.mark.django_db
def test_product_update_user(api_user, product_factory):

    product = product_factory()
    params = {'name': 'Test_product'}
    url = reverse('products-detail', args=(product.id,))
    resp = api_user.patch(url, params)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест на удаление товара с авторизацией админа
@pytest.mark.django_db
def test_product_delete_admin(api_admin, product_factory):
    product = product_factory()
    url = reverse("products-detail", args=(product.id, ))
    resp = api_admin.delete(url, {"id": product.id})
    assert resp.status_code == HTTP_204_NO_CONTENT


# тест на удаление товара с авторизацией юзера
@pytest.mark.django_db
def test_product_delete_admin(api_user, product_factory):
    product = product_factory()
    url = reverse("products-detail", args=(product.id, ))
    resp = api_user.delete(url, {"id": product.id})
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест на получение определенного товара
@pytest.mark.django_db
def test_product_get(api_client, product_factory):
    product = product_factory()
    url = reverse("products-detail", args=(product.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert resp_json['id'] == product.id


# тест на получение всех отзывов
@pytest.mark.django_db
def test_review_list(client):
    url = reverse('reviews-list')
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK


# тест на получение определенного отзыва
@pytest.mark.django_db
def test_review_get(api_client, review_factory):
    review = review_factory()
    url = reverse("reviews-detail", args=(review.id,))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert resp_json['id'] == review.id


# тест на создание отзыва с авторизацией
@pytest.mark.django_db
def test_review_post_auth(api_user, product_factory):
    product = product_factory(_quantity=2)
    review_payload = {
        'review': product[0].id,
        'text': 'desc for test_product',
        'mark': 1,
    }

    url = reverse('reviews-list')

    resp = api_user.post(url, review_payload)
    assert resp.status_code == HTTP_201_CREATED


# тест на создание отзыва без авторизации
@pytest.mark.django_db
def test_review_post_no_auth(api_client):

    review_payload = {
        'review': 1,
        'text': 'desc for test_product',
        'mark': 1,
    }

    url = reverse('reviews-list')

    resp = api_client.post(url, review_payload)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


# тест на обновление своего отзыва
# тест на создание двух отзывов к 1 товару
@pytest.mark.django_db
def test_order_create_auth(api_user, api_admin, review_factory, product_factory):
    product = product_factory()
    review = review_factory()
    url = reverse('reviews-list')
    rev_data = {
        'review': review.review['id'],
        'text': 'test',
        'mark': 2
    }
    resp = api_admin.post(url, rev_data)
    assert resp.status_code == HTTP_201_CREATED



# тест на создание заказа с авторизацией
# @pytest.mark.django_db
# def test_order_create_auth(api_user, order_factory, product_factory):
#     product = product_factory()
#     order_payload = {
#         "positions": [
#             {"product_id": product.id, "quantity": 2},
#         ]
#     }
#     url = reverse('orders-list')
#     resp = api_user.post(url, order_payload)
#     assert resp.status_code == HTTP_201_CREATED



