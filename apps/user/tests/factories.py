import factory
from faker import Faker
from pytest_factoryboy import register

from django.contrib.auth import get_user_model

fake = Faker()


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda num: f'User #{num}')
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()

    class Meta:
        model = get_user_model()

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password('password')
