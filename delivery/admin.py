from django.contrib import admin

from .models import(
    Category,
    Restaurant,
    Food,
    Order,
    Status,
    Report,
    Discounts,
    Users,
    CartProduct,
    Cart,
    Small_order,
)

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Status)
admin.site.register(Report)
admin.site.register(Discounts)
admin.site.register(Users)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Small_order)
