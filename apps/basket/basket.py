from decimal import Decimal

from apps.shop.models import Product


class Basket:
    """A base Basket class, providing some default behaviors for a user basket in a session"""

    def __init__(self, request):
        self.session = request.session

        if 'basket' not in request.session:
            self.basket = self.session['basket'] = {}
        else:
            self.basket = self.session['basket']

    def add_product(self, product: Product, quantity: int = 1) -> None:
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id] = {'title': product.title, 'price': str(product.price), 'quantity': quantity}
        self.save()

    def add_quantity(self, product: Product, quantity: int) -> None:
        product_id = str(product.id)

        if product_id not in self.basket:
            raise KeyError(f"There are no {product.title} in the user's basket")

        self.basket[product_id]['quantity'] += quantity
        self.save()

    def delete_product(self, product: Product) -> None:
        product_id = str(product.id)

        if product_id not in self.basket:
            raise KeyError(f"There are no {product.title} in the user's basket")

        del self.basket[product_id]
        self.save()

    def save(self) -> None:
        self.session.modified = True

    def get_total_price(self) -> Decimal:
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def get_total_quantity(self) -> int:
        return sum(item['quantity'] for item in self.basket.values())

    def keys(self):
        return self.basket.keys()

    def values(self):
        return self.basket.values()

    def items(self):
        return self.basket.items()

    def __getitem__(self, item):
        return self.basket[item]

    def __setitem__(self, key, value):
        self.basket[key] = value

    def __delitem__(self, key):
        del self.basket[key]
