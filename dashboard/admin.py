from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Customer, Product, ShippingAddress,Category, Order, OrderItem

#Child inline classes
class ShippingInline(admin.StackedInline):
	model = ShippingAddress
	extra = 1

class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 1

class OrderInline(admin.StackedInline):
	model = Order
	extra = 1



#Parent Inline view Classes
class OrderView(admin.ModelAdmin):
	inlines = [ OrderItemInline, ShippingInline ]


class CustomerView(admin.ModelAdmin):
	inlines = [OrderInline, ]



#General Admin  Classes
class OrderAdmin(ImportExportModelAdmin, OrderView):
	pass

class CustomerAdmin(ImportExportModelAdmin, CustomerView):
	pass

class OrderItemAdmin(ImportExportModelAdmin):
	pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Category)
