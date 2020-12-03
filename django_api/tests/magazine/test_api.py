import pytest

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, \
    HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_201_CREATED

from magazine.models import Product, ProductReviews, Orders, Collections

# ____________Tests for products____________
# тест на получение всех товаров
@pytest.mark.django_db
def test_product_list(api_client):
    url = reverse('products-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


# # тест на создание товаров в базе данных
@pytest.mark.django_db
def test_product_create(api_client):
    product = Product.objects.bulk_create([
        Product(name='Test_product_1', price=1000),
        Product(name='Test_product_2', price=2000),
        ])
    url = reverse('products-list')
    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 2
    assert resp_json[0]['name'] == product[0].name


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


# ____________Tests for reviews____________
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

# тест на удаление отзыва своего/чужого








# ____________Tests for orders____________
# тест на получение списка заказов без авторизации
@pytest.mark.django_db
def test_order_list_no_auth(api_client):

    url = reverse('orders-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


# тест на получение списка заказов с авторизацией
@pytest.mark.django_db
def test_order_list_auth(api_user):

    url = reverse('orders-list')
    resp = api_user.get(url)
    assert resp.status_code == HTTP_200_OK


# тест на получение своего заказа!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# тест на создание заказа с авторизацией
@pytest.mark.django_db
def test_order_create_auth(api_user, order_factory, product_factory):
    product = product_factory()
    order_payload = {
        "id": 1,
        "positions": [
            {"product_id": product.id, "quantity": 2},
        ]
    }
    url = reverse('orders-list')
    resp = api_user.post(url, order_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json['id'] == order_payload['id']


# тест на  создание заказа без авторизаяции
@pytest.mark.django_db
def test_order_create_no_auth(api_client, product_factory):
    product = product_factory()
    order_payload = {
        "positions": [
            {"product_id": product.id, "quantity": 2},
        ]
    }
    url = reverse('orders-list')
    resp = api_client.post(url, order_payload, format='json')
    assert resp.status_code == HTTP_401_UNAUTHORIZED





# тест на изменение заказа юзером!!!!!!!!!!!!!!!!!!!!!!!!!

# тест на удаление заказа админом!!!!!!!!!!!!!!!!!!!!!!!!!

# тест на удаление заказа юзером!!!!!!!!!!!!!!!!!!!!!!!!!!


# ____________Tests for collections____________
# тест на получение всех подборок
@pytest.mark.django_db
def test_collection_list(api_client):

    url = reverse('collections-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK


# тест на создание подборки админом
@pytest.mark.django_db
def test_collection_post_admin(api_admin, product_factory):
    product = product_factory(_quantity=2)
    collection_payload = {
        'id': 1,
        'title': 'test_collection',
        'text': 'desc for collection',
        'products': [
            product[0].id,
            product[1].id
        ]
    }
    url = reverse('collections-list')
    resp = api_admin.post(url, collection_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json['title'] == collection_payload['title']


# тест на создание подборки юзером
@pytest.mark.django_db
def test_collection_post_user(api_user, product_factory):

    product = product_factory(_quantity=3)
    collection_payload = {
        'id': 1,
        'title': 'test_collection',
        'text': 'desc for collection',
        'products': [
            product[0].id,
            product[1].id
        ]
    }
    url = reverse('collections-list')
    resp = api_user.post(url, collection_payload, format='json')
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест на изменение подборки админом
@pytest.mark.django_db
def test_collection_update_admin(api_admin, collection_factory):

    collection = collection_factory()
    params = {'title': 'Test_product'}
    url = reverse('collections-detail', args=(collection.id,))
    resp = api_admin.patch(url, params)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['title'] == params['title']


# тест на изменение подборки юзером
@pytest.mark.django_db
def test_collections_update_user(api_user, collection_factory):

    collection = collection_factory()
    params = {'title': 'Test_product'}
    url = reverse('collections-detail', args=(collection.id,))
    resp = api_user.patch(url, params)
    assert resp.status_code == HTTP_403_FORBIDDEN


# тест на удаление подборки админом
@pytest.mark.django_db
def test_collections_delete_user(api_admin, collection_factory):

    collection = collection_factory()
    url = reverse('collections-detail', args=(collection.id,))
    resp = api_admin.patch(url, {"id": collection.id})
    assert resp.status_code == HTTP_204_NO_CONTENT


# тест на удаление подборки юзером
@pytest.mark.django_db
def test_collections_delete_user(api_user, collection_factory):

    collection = collection_factory()
    url = reverse('collections-detail', args=(collection.id,))
    resp = api_user.patch(url, {"id": collection.id})
    assert resp.status_code == HTTP_403_FORBIDDEN






###################################################################
# тест на обновление своего/чужого отзыва!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@pytest.mark.django_db
def test_update_review(api_admin, review_factory):
    review = review_factory()
    params = {'text': 'Test_product'}
    url = reverse('reviews-detail', args=(review.id,))
    resp = api_admin.patch(url, params)
    assert resp.status_code == HTTP_200_OK

    
# тест на изменение заказа админом!!!!!!!!!!!!!!!!!!!!!!!!
@pytest.mark.django_db
def test_order_update_admin(api_admin, order_factory, product_factory):
    product = product_factory()
    order_payload = {
        "id": 1,
        "positions": [
            {"product_id": product.id, "quantity": 2},
        ]
    }
    order = {
        "positions": [
            {"quantity": 3},
        ]
    }
    url = reverse('orders-detail', args=(order_payload['id'],))
    resp = api_admin.patch(url, order, format='json')
    assert resp.status_code == HTTP_200_OK
    
    
 # тест на создание двух отзывов к 1 товару!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@pytest.mark.django_db
def test_review_double_post(api_user, review_factory, product_factory):
    product = product_factory(_quantity=2)
    review = review_factory(review=product[0].id)
    url = reverse('reviews-list')
    new_review = {
        'review': review.review.id,
        'text': 'test',
        'mark': 1
    }
    resp = api_user.post(url, new_review)
    assert resp.status_code == HTTP_201_CREATED
