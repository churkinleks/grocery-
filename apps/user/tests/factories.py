import factory
from pytest_factoryboy import register

from django.contrib.auth import get_user_model

from conftest import faker


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda num: f'User #{num}')
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: (faker.last_name()))
    email = factory.LazyAttribute(lambda _: (faker.email()))

    class Meta:
        model = get_user_model()

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if create:
            password: str = extracted or 'password'
            self.set_password(password)
