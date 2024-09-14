from unidecode import unidecode

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Catalog(models.Model):
    title = models.CharField(max_length=20, verbose_name=_('title'))
    upper_catalog = models.ForeignKey(
        'self',
        related_name='subdirectories',
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True,
        verbose_name=_('upper catalog'),
    )

    class Meta:
        unique_together = ('title', 'upper_catalog')
        verbose_name = _('catalog')
        verbose_name_plural = _('catalogs')

    def clean(self):
        nesting_level = 0
        catalog = self
        while catalog.upper_catalog:
            nesting_level += 1
            catalog = catalog.upper_catalog
            if nesting_level > 1:
                raise ValidationError({'upper_catalog': _('The maximum nesting level is 1')})

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    quantity = models.PositiveSmallIntegerField(verbose_name=_('quantity'))
    catalog = models.ForeignKey(Catalog, related_name='products', on_delete=models.PROTECT, verbose_name=_('catalog'))
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('price'),
    )
    image = models.ImageField(
        upload_to='products/images',
        default='products/images/default.jpg',
        verbose_name=_('image'),
        validators=[
            FileExtensionValidator(
                allowed_extensions=('jpg', 'png'),
                message=_("Can only be saved in 'jpg' or 'png' format"),
            ),
        ],
    )
    specification = models.FileField(
        upload_to='products/specifications',
        default=None,
        blank=True,
        null=True,
        verbose_name=_('specification'),
        validators=[
            FileExtensionValidator(allowed_extensions=('pdf',), message=_("Can only be saved in 'pdf' format")),
        ],
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return f'{self.title} ({self.price} $, {self.quantity} pcs)'


class Promotion(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    products = models.ManyToManyField(Product, related_name='promotions', verbose_name=_('products'))
    active = models.BooleanField(default=False, null=False, verbose_name=_('active'))
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name=_('price'),
        validators=[MinValueValidator(0)],
    )
    slug = models.SlugField(max_length=100, default='', null=False, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')

    def save(self, *args, **kwargs):
        """Translates the value of the title attribute (from any languages) in the slug form"""
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:promotion_detail', args=(self.slug,))

    def __str__(self):
        return f'{self.title}: {self.price}$'
