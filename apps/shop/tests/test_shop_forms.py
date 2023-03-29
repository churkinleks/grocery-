import pytest

from apps.shop.forms import PriceFilterForm


@pytest.mark.parametrize(
    'price_from, price_to, validity',
    (
        (None, None, True),
        (0, None, True),
        (1.22, None, True),
        (10000, None, True),
        (None, 0, True),
        (None, 1.23, True),
        (None, 10000, True),
        (0, 0.11, True),
        (1, 1.22, True),
        (0, 1, True),
        (0, 10000, True),
        (1, 10000, True),
        (10000, 10000, True),
        (0, 1.222, False),
        (1, 1.222, False),
        (1.222, None, False),
        (1.222, 2, False),
        (1, 0, False),
        (10000, 0, False),
        (10000, 1, False),
        (-1, 0, False),
        (-1, None, False),
        (0, -1, False),
        (None, -1, False),
        ('text', 0, False),
        (0, 'text', False),
    ),
)
def test_price_filer_form(price_from, price_to, validity):
    form = PriceFilterForm(
        data={
            'price_from': price_from,
            'price_to': price_to,
        }
    )
    assert form.is_valid() == validity
