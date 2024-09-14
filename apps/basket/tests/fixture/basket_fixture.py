import pytest

from apps.basket.basket import Basket


@pytest.fixture
def user_basket(client, auth_user, product):
    user_basket = Basket(client)
    user_basket.add_product(product)
    user_basket.session.save()
    return user_basket
