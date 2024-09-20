from unidecode import unidecode

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    DecimalField,
    FileField,
    ForeignKey,
    ImageField,
    Manager,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    SlugField,
    TextField,
    UniqueConstraint,
)
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


# TODO(Aleksei Churkin): Maybe better to try django-types because anyway it's work from django-types
# and so mypy should work correcltly.
class Catalog(Model):
    # PyRight
    id: int
    top_catalog_id: int | None
    subcatalogs: Manager['Catalog']
    products: Manager['Product']

    top_catalog = ForeignKey(
        'self',
        on_delete=PROTECT,
        related_name='subcatalogs',
        null=True,
        default=None,
        verbose_name=_('Top catalog'),
    )

    title = CharField(_('Title'), max_length=20)

    class Meta:
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')
        constraints = [
            UniqueConstraint(fields=['title', 'top_catalog'], name='catalog_unique_title_top_catalog'),
        ]

    def __str__(self) -> str:
        return f'{self.title}'

    def clean(self) -> None:
        nesting_level: int = 0
        catalog: Catalog = self

        while catalog.top_catalog:
            nesting_level += 1
            catalog = catalog.top_catalog

            if nesting_level > 1:
                raise ValidationError({'top_catalog': _('The maximum nesting level is 1.')})


class Product(Model):
    # PyRight
    id: int
    catalog_id: int
    promotions: Manager['Promotion']

    catalog = ForeignKey(Catalog, PROTECT, related_name='products', verbose_name=_('Catalog'))

    title = CharField(_('Title'), max_length=50)
    description = TextField(_('Description'))
    quantity = PositiveSmallIntegerField(_('Quantity'))
    price = DecimalField(_('Price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = ImageField(
        verbose_name=_('Image'),
        upload_to='products/images',
        default='products/images/default.jpg',
        validators=[
            FileExtensionValidator(
                allowed_extensions=('jpg', 'png'),
                message=_("Can only be saved in 'jpg' or 'png' format"),
            ),
        ],
    )
    specification = FileField(
        verbose_name=_('Specification'),
        upload_to='products/specifications',
        null=True,
        default=None,
        validators=[
            FileExtensionValidator(allowed_extensions=('pdf',), message=_("Can only be saved in 'pdf' format")),
        ],
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self) -> str:
        return f'{self.title} ({self.price} $, {self.quantity} pcs.)'


class Promotion(Model):
    # PyRight
    id: int

    products = ManyToManyField('Product', related_name='promotions', verbose_name=_('Products'))

    title = CharField(_('Title'), max_length=50)
    description = TextField(_('Description'))
    active = BooleanField(_('Active'), default=False)
    price = DecimalField(('Price'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    slug = SlugField(_('Slug'), max_length=100, default='')

    class Meta:
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')

    def __str__(self) -> str:
        return f'{self.title}: {self.price}$'

    def save(self, *args, **kwargs) -> None:
        """Translates the value of the title attribute (from any languages) in the slug form."""
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('shop:promotions_detail', args=(self.slug,))
