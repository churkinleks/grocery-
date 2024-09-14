from typing import Optional

from django.db.models import QuerySet

# ----- FILTERS -----


def filter_products_by_price(price_from: Optional[int], price_to: Optional[int], products: QuerySet) -> QuerySet:
    price_from, price_to = price_from or 0, price_to or 10_000
    return products.filter(price__gte=price_from, price__lte=price_to)
