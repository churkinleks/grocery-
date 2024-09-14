from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import View

from ..basket.basket import Basket
from .forms import PriceFilterForm
from .models import Product, Promotion
from .services import filter_products_by_price


class DashboardView(View):
    def get(self, request):
        product_ids_in_basket = list()
        price_form = PriceFilterForm(request.GET)
        products = Product.objects.all().defer('quantity', 'catalog', 'specification')

        if request.user.is_authenticated:
            user_basket = Basket(request)
            product_ids_in_basket = [int(item) for item in user_basket.keys()]

        if price_form.is_valid() and price_form.has_changed():
            price_from = price_form.cleaned_data.get('price_from')
            price_to = price_form.cleaned_data.get('price_to')
            products = filter_products_by_price(price_from, price_to, products)

        context = {'product_ids_in_basket': product_ids_in_basket, 'price_form': price_form, 'products': products}
        return render(request, 'shop/dashboard.html', context=context)

    def post(self, request):
        product_id_to_purchase = request.POST['product_id_to_purchase']
        product = get_object_or_404(Product, id=product_id_to_purchase)

        user_basket = Basket(request)
        user_basket.add_product(product)

        return redirect('shop:dashboard')


def promotion_list_view(request):
    promotions = (
        Promotion.objects.prefetch_related(Prefetch('products', queryset=Product.objects.all().only('title')))
        .filter(active=True)
        .defer(
            'description',
            'active',
        )
    )
    return render(request, 'shop/promotion/list.html', context={'promotions': promotions})


def promotion_detail_view(request, slug):
    promotion = get_object_or_404(Promotion, slug=slug)

    if not promotion.active:
        raise Http404(_('The requested promotion is inactive'))
    return render(request, 'shop/promotion/detail.html', context={'promotion': promotion})
