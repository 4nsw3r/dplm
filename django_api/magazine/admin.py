from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Orders, Product, ProductOrderPosition, ProductReviews


class OrderInline(admin.TabularInline):
    model = ProductOrderPosition
    extra = 1

    
@admin.register(Orders)
class ProdAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ('id', 'status')

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        obj.save()


@admin.register(ProductReviews)
class RevAdmin(admin.ModelAdmin):
    pass