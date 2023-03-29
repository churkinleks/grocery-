from django.shortcuts import render, redirect

from .forms import BasketFormSet
from .basket import Basket


def detail_basket(request):
    if request.user.is_anonymous:
        return render(request, 'basket/anonymous.html')

    user_basket = Basket(request)
    initial_data = [{'id': key, **value} for key, value in user_basket.items()]
    basket_form_set = BasketFormSet(initial=initial_data)

    if request.method == 'POST':
        basket_form_set = BasketFormSet(request.POST, initial=initial_data)
        if basket_form_set.is_valid():
            _process_user_basket(user_basket, basket_form_set)
            user_basket.save()
            return redirect('basket:detail')

    context = {
        'basket_form_set': basket_form_set,
        'total_price': user_basket.get_total_price(),
    }
    return render(request, 'basket/detail.html', context=context)


def _process_user_basket(user_basket: Basket, basket_form_set: BasketFormSet) -> None:
    for form_item in basket_form_set.cleaned_data:
        basket_item: dict = user_basket[form_item['id']]
        basket_item['quantity'] = form_item['quantity']
        if form_item['DELETE']:
            del user_basket[form_item['id']]
