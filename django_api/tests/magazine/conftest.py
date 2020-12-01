import pytest
from model_bakery import baker


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
