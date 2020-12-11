import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture
def api_client():
    """Фикстура для клиента API."""
    return APIClient()


@pytest.fixture
def token_admin(admin_user):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=admin_user)
    return token.key


@pytest.fixture
def api_admin(token_admin):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token_admin}')
    return client


@pytest.fixture
def api_user(django_user_model):
    client = APIClient()
    username = 'user1'
    password = '123'
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=False)
    user_token = Token.objects.create(user=user)
    client.force_login(user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    return client


@pytest.fixture
def user(django_user_model):
    username = 'user2'
    password = '123'
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=False)
    return user


@pytest.fixture
def apiuser(django_user_model, user):
    client = APIClient()
    usertoken = Token.objects.create(user=user)
    client.force_login(user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {usertoken.key}')
    return client


@pytest.fixture
def order_prod_factory(user):
    def factory(min_amount=1, max_amount=20, **kwargs):
        return baker.make('Order', user=user, **kwargs, make_m2m=True)
    return factory