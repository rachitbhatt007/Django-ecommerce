from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display=('name','price','quantity')


class SellerAdminArea(admin.AdminSite):
    site_header = "Seller Site"


seller_site = SellerAdminArea(name="SellerAdmin")


class ProductPermissions(admin.ModelAdmin):
    list_display=('name','price','quantity')
    def has_module_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class OrderPermissions(admin.ModelAdmin):
    list_display = ('id','user','order_date')
    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','order_date')

class OrderitemAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','ordered')    

seller_site.register(Product, ProductPermissions)
seller_site.register(Order, OrderPermissions)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderitemAdmin)
