from django.contrib import admin
from .models import CustomUser, Category, Item, Hall, Table, Booking, Order, OrderItem

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Hall)
admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(OrderItem)
