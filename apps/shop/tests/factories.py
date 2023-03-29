import factory
from faker import Faker
from pytest_factoryboy import register

from apps.shop.models import Catalog, Product, Promotion

fake = Faker()


@register
class CatalogFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda num: f'Catalog #{num}')
    upper_catalog = None

    class Meta:
        model = Catalog


@register
class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda num: f'Product #{num}')
    price = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    quantity = fake.random_int(1, 100)
    description = fake.text(500)
    catalog = factory.SubFactory(CatalogFactory)
    # image - default
    # specification - default

    class Meta:
        model = Product


@register
class PromotionFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda num: f'Promotion #{num}')
    description = fake.text(500)
    price = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
    active = fake.pybool()
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
