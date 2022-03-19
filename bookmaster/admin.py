from django.contrib import admin
# from .models import ProductReview

# Register your models here.

from .models import *
# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Genre)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

# class ProductReviewAdmin(admin.ModelAdmin):
# 	list_display = ('user', 'product', 'review_text', 'get_review_rating')
# admin.site.register(ProductReview, ProductReviewAdmin)