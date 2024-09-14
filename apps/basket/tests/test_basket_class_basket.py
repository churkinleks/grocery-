import pytest


@pytest.mark.django_db
class TestBasket:
    def test_add_product(self, product, user_basket):
        basket_data = {str(product.id): {'title': product.title, 'price': str(product.price), 'quantity': 1}}
        assert user_basket.basket == basket_data

    def test_add_the_same_product(self, product, user_basket):
        user_basket.add_product(product)
        basket_data = {str(product.id): {'title': product.title, 'price': str(product.price), 'quantity': 1}}
        assert user_basket.basket == basket_data

    def test_add_quantity(self, product, user_basket):
        user_basket.add_quantity(product, quantity=132)
        basket_data = {str(product.id): {'title': product.title, 'price': str(product.price), 'quantity': 133}}
        assert user_basket.basket == basket_data

    def test_add_quantity_error(self, product_factory, user_basket):
        product = product_factory()
        with pytest.raises(KeyError):
            user_basket.add_quantity(product, quantity=132)

    def test_delete_product(self, product, user_basket):
        user_basket.delete_product(product)
        assert user_basket.basket == {}

    def test_delete_product_error(self, product_factory, user_basket):
        product = product_factory()
        with pytest.raises(KeyError):
            user_basket.delete_product(product)

    def test_get_total_price(self, product_factory, product, user_basket):
        product_2 = product_factory()
        user_basket.add_product(product_2, quantity=5)
        assert user_basket.get_total_price() == product.price * 1 + product_2.price * 5

    def test_get_total_quantity(self, product_factory, user_basket):
        product_2 = product_factory()
        user_basket.add_product(product_2, quantity=5)
        assert user_basket.get_total_quantity() == 1 + 5

    def test_save(self, user_basket):
        user_basket.session.modified = False
        user_basket.save()
        assert user_basket.session.modified is True
