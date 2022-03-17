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
admin.site.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'post', 'created', 'active')
#     list_filter = ('active', 'created', 'updated')
#     search_fields = ('name', 'email', 'body')
# # admin.site.register(Comment, CommentAdmin)

# class ProductReviewAdmin(admin.ModelAdmin):
# 	list_display = ('user', 'product', 'review_text', 'get_review_rating')
# admin.site.register(ProductReview, ProductReviewAdmin)