import pytest
from model_bakery import baker
from tests.conftest import user, apiuser


@pytest.fixture()
def product_factory():
    def factory(**kwargs):
        product = baker.make("magazine.Product", **kwargs)
        return product
    return factory


@pytest.fixture()
def review_factory():
    def factory(**kwargs):
        review = baker.make("magazine.ProductReviews", **kwargs)
        return review
    return factory


@pytest.fixture()
def order_factory():
    def factory(**kwargs):
        order = baker.make("magazine.Orders", **kwargs)
        return order
    return factory


@pytest.fixture()
def collection_factory():
    def factory(**kwargs):
        collection = baker.make("magazine.Collections", **kwargs)
        return collection
    return factory


# @pytest.fixture()
# def order_prod_factory():
#     def factory(**kwargs):
#         #prod_set = baker.prepare("magazine.Product")
#         orders_set = baker.make("magazine.Orders", products__id=1, products__created_at='2020-12-07', products__name='milk')
#         return orders_set
#     return factory





@pytest.fixture
def order_prod_factory(user):
    def factory(**kwargs):
        return baker.make('magazine.Orders', creator=user, **kwargs, make_m2m=True)
    return factory