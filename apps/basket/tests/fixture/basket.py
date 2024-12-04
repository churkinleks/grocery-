import pytest

from apps.basket.basket import Basket


@pytest.fixture
def user_basket(client, auth_user, product):
    user_basket = Basket(client)
    user_basket.add_product(product)
    user_basket._session.save()  # TODO(Aleksei Churkin): Change access method.  # noqa: SLF001
    return user_basket
