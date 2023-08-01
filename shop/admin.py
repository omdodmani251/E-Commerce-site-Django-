from django.contrib import admin

# Register your models here.
from . models import Product,Feedback,Order,Order_tracker
admin.site.register(Product)
admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(Order_tracker)