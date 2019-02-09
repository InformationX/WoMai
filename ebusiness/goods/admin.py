from django.contrib import admin
from .models import Address, Goods, User, Orders, Order
# Register your models here.


admin.site.register(Address)
admin.site.register(Goods)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Orders)