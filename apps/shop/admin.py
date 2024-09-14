from django.contrib import admin, messages
from django.db.models import QuerySet

from .models import Catalog, Product, Promotion


class QuantityFilter(admin.SimpleListFilter):
    title = 'quantity'
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return [
            ('0-9', '<10'),
            ('10-50', '10-50'),
            ('50-100', '50-100'),
            ('100+', '100+'),
        ]

    def queryset(self, request, queryset: QuerySet):
        value = self.value()
        if value:
            if value != '100+':
                low_limit, top_limit = value.split('-')
                queryset = queryset.filter(quantity__gte=low_limit, quantity__lte=top_limit)
            else:
                queryset = queryset.filter(quantity__gt=100)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'catalog', 'is_it_in_promotion')
    list_editable = ('price', 'quantity')
    readonly_fields = ('get_promotion_type',)
    fieldsets = (
        (None, {'fields': ('title', 'price', 'quantity', 'description', 'catalog', 'get_promotion_type', 'image')}),
        ('Technical information', {'fields': ('specification',), 'classes': ('collapse',)}),
    )
    list_per_page = 25
    show_full_result_count = False

    search_fields = ('title',)
    list_filter = (QuantityFilter,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('promotions')

    @admin.display(boolean=True, description='In the promotion?')
    def is_it_in_promotion(self, product: Product) -> bool:
        if product.promotions.all():
            return True
        return False

    @admin.display(description='Current promotions')
    def get_promotion_type(self, product: Product) -> str:
        promotions = product.promotions.all()
        if promotions:
            return '\n'.join(f'* {i}' for i in promotions)
        return 'Not in the promotion'


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_it_subdirectory')
    readonly_fields = ('get_products', 'get_subdirectories')
    search_fields = ('title',)
    list_filter = (('upper_catalog', admin.RelatedOnlyFieldListFilter),)
    show_full_result_count = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('upper_catalog')

    @admin.display(boolean=True, description='Subdirectory?')
    def is_it_subdirectory(self, catalog: Catalog) -> bool:
        if catalog.upper_catalog:
            return True
        return False

    @admin.display(description='Subdirectories')
    def get_subdirectories(self, catalog: Catalog) -> str:
        subdirectories = catalog.subdirectories.all()
        if subdirectories:
            return '\n'.join(f'* {i}' for i in subdirectories)
        return 'No subdirectories'

    @admin.display(description='Products in the catalog')
    def get_products(self, catalog: Catalog) -> str:
        products = catalog.products.all()
        if products:
            return '\n'.join(f'* {i}' for i in products)
        return 'No products'


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active')
    ordering = ('-active',)
    exclude = ('slug',)
    search_fields = ('title',)
    actions = ('set_to_active', 'set_inactive')
    filter_horizontal = ('products',)
    show_full_result_count = False

    @admin.action(description='Make active')
    def set_to_active(self, request, qs: QuerySet):
        number_of_changes = qs.update(active=True)
        self.message_user(request, f'Changes have been made- {number_of_changes}', level=messages.SUCCESS)

    @admin.action(description='Make inactive')
    def set_inactive(self, request, qs: QuerySet):
        number_of_changes = qs.update(active=False)
        self.message_user(request, f'Changes have been made - {number_of_changes}', level=messages.SUCCESS)
