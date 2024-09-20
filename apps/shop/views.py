from django.db.models import Prefetch, QuerySet
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import View

from apps.basket.basket import Basket
from apps.shop.forms import PriceFilterForm
from apps.shop.models import Product, Promotion


class DashboardView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        product_ids_in_basket: list[int] = list()

        if request.user.is_authenticated:
            user_basket: Basket = Basket(request)
            product_ids_in_basket = [int(item) for item in user_basket.keys()]

        price_form: PriceFilterForm = PriceFilterForm(request.GET)
        products: QuerySet[Product] = Product.objects.all().defer('quantity', 'catalog', 'specification')

        if price_form.is_valid() and price_form.has_changed():
            price_from: int = price_form.cleaned_data.get('price_from') or 0
            price_to: int = price_form.cleaned_data.get('price_to') or 10_000
            products = products.filter(price__gte=price_from, price__lte=price_to)

        context: dict = {'product_ids_in_basket': product_ids_in_basket, 'price_form': price_form, 'products': products}
        return render(request, 'shop/dashboard.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        product_id_to_purchase: str = request.POST['product_id_to_purchase']
        product: Product = get_object_or_404(Product, id=product_id_to_purchase)

        user_basket: Basket = Basket(request)
        user_basket.add_product(product)

        return redirect('shop:dashboard')


def promotions(request: HttpRequest) -> HttpResponse:
    promotions: QuerySet[Promotion] = (
        Promotion.objects.prefetch_related(Prefetch('products', queryset=Product.objects.all().only('title')))
        .filter(active=True)
        .defer(
            'description',
            'active',
        )
    )
    return render(request, 'shop/promotions/all.html', context={'promotions': promotions})


def promotions_detail(request: HttpRequest, slug: str) -> HttpResponse:
    promotion: Promotion = get_object_or_404(Promotion, slug=slug)

    if not promotion.active:
        raise Http404(_('The requested promotion is inactive.'))
    return render(request, 'shop/promotions/detail.html', context={'promotion': promotion})
