from faker import Faker

pytest_plugins: tuple[str, ...] = (
    'apps.shop.tests.fixture.api',
    'apps.user.tests.fixture.models',
    'apps.basket.tests.fixture.basket',
    'apps.shop.tests.factories',
    'apps.user.tests.factories',
)

# Use only one instance of Faker for all tests `from conftest import faker`.
faker: Faker = Faker()
