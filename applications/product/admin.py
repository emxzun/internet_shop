from django.contrib import admin

from applications.product.models import Product, Comment, Review, Rating, Like

admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Like)
