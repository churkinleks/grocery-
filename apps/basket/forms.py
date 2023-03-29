from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _


class BasketForm(forms.Form):
    id = forms.CharField(disabled=True,
                         widget=forms.HiddenInput)
    title = forms.CharField(disabled=True)
    price = forms.DecimalField(disabled=True)
    quantity = forms.IntegerField(min_value=0,
                                  label=_('Quantity'),
                                  widget=forms.NumberInput(attrs={'class': 'input '}))


BasketFormSet = formset_factory(BasketForm, extra=0, can_delete=True)
