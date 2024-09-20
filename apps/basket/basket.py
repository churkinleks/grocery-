from decimal import Decimal

from _collections_abc import dict_items, dict_keys, dict_values

from django.http import HttpRequest

from apps.shop.models import Product


class Basket:
    """A base Basket class, providing some default behaviors for a user basket in a session."""

    def __init__(self, request: HttpRequest) -> None:
        self._session = request.session
        self._basket = self._session.setdefault('basket', {})

    def add_product(self, product: Product, quantity: int = 1) -> None:
        product_id: str = str(product.id)

        if product_id in self._basket:
            self._basket[product_id]['quantity'] = quantity
        else:
            self._basket[product_id] = {'title': product.title, 'price': str(product.price), 'quantity': quantity}
        self.save()

    def add_quantity(self, product: Product, quantity: int) -> None:
        product_id: str = str(product.id)

        if product_id not in self._basket:
            raise KeyError(f"There are no {product.title} in the user's basket")

        self._basket[product_id]['quantity'] += quantity
        self.save()

    def delete_product(self, product: Product) -> None:
        product_id: str = str(product.id)

        if product_id not in self._basket:
            raise KeyError(f"There are no {product.title} in the user's basket")

        del self._basket[product_id]
        self.save()

    def save(self) -> None:
        self._session.modified = True

    def get_total_price(self) -> Decimal:
        total_price: int = sum(Decimal(item['price']) * item['quantity'] for item in self._basket.values())
        return Decimal(total_price)

    def get_total_quantity(self) -> int:
        return sum(item['quantity'] for item in self._basket.values())

    def keys(self) -> dict_keys:
        return self._basket.keys()

    def values(self) -> dict_values:
        return self._basket.values()

    def items(self) -> dict_items:
        return self._basket.items()

    def __getitem__(self, item):
        return self._basket[item]

    def __setitem__(self, key, value):
        self._basket[key] = value

    def __delitem__(self, key):
        del self._basket[key]
