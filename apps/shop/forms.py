from django import forms
from django.utils.translation import gettext_lazy as _


class PriceFilterForm(forms.Form):
    price_from = forms.DecimalField(
        label=_('From'),
        min_value=0,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'input'}),
        error_messages={'min_value': _('The price cannot be lower than 0')},
    )

    price_to = forms.DecimalField(
        label=_('To'),
        min_value=0,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'input'}),
        error_messages={'min_value': _('The price cannot be lower than 0')},
    )

    def clean(self):
        """If the price 'To' is less than the price 'From', an error will be added to the form"""
        if self.is_valid() and self.has_changed():
            price_from = self.cleaned_data.get('price_from')
            price_to = self.cleaned_data.get('price_to')
            if price_from and price_to is not None and price_from > price_to:
                self.add_error('price_to', _("The price 'To' should be greater than the price 'From'"))
        return self.cleaned_data
