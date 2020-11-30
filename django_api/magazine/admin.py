from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Orders, Product, ProductOrderPosition, ProductReviews, Collections


class OrderInline(admin.TabularInline):
    model = ProductOrderPosition
    extra = 1

    
@admin.register(Orders)
class ProdAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ('id', 'status')
    readonly_fields = ('order_sum', 'id')
    
    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        obj.save()


@admin.register(ProductReviews)
class RevAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProdAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Collections)
class CollectionsAdmin(admin.ModelAdmin):
    pass