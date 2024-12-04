from decimal import Decimal

import factory
from pytest_factoryboy import register

from apps.shop.models import Catalog, Product, Promotion
from conftest import faker


@register
class CatalogFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda num: f'Catalog #{num}')
    top_catalog = None

    class Meta:
        model = Catalog


@register
class ProductFactory(factory.django.DjangoModelFactory):
    catalog = factory.SubFactory(CatalogFactory)

    title = factory.Sequence(lambda num: f'Product #{num}')
    price = factory.LazyAttribute(lambda _: faker.pydecimal(left_digits=2, right_digits=2, positive=True))
    quantity = factory.LazyAttribute(lambda _: faker.random_int(1, 100))
    description = factory.LazyAttribute(lambda _: faker.text(500))
    # image - default
    # specification - default

    class Meta:
        model = Product

    class Params:
        cheap_and_last = factory.Trait(
            price=Decimal(1),
            quantity=1,
        )


@register
class PromotionFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda num: f'Promotion #{num}')
    description = factory.LazyAttribute(lambda _: faker.text(500))
    price = factory.LazyAttribute(lambda _: faker.pydecimal(left_digits=2, right_digits=2, positive=True))
    active = factory.LazyAttribute(lambda _: faker.pybool())
    # slug - default

    class Meta:
        model = Promotion

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            product_1 = ProductFactory()
            product_2 = ProductFactory()
            self.products.add(product_1, product_2)
        else:
            self.products.add(*extracted)
