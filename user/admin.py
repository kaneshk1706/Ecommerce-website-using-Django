from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced,Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','img','desc','price','dis_price','offer','category']
    class Media:
        js = ('static/js/myscript/product_validation.js',)



@admin.register(Customer)
class CusotmerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','Address','city','state','pincode']


@admin.register(Cart)

class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products','quantity']
    def products(self,obj):
        link = reverse("admin:user_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.name)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']

    def customer(self, obj):
        link = reverse("admin:user_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product(self, obj):
        link = reverse("admin:user_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.name)

    def payment(self, obj):
        link = reverse("admin:user_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, obj.payment.razorpay_payment_id)
    
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products']
    def products(self,obj):
        link = reverse("admin:user_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.name)
    


# admin.py
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'admin_reply')
    list_filter = ('admin_reply',)
    search_fields = ('email', 'message')
    readonly_fields = ('email', 'message')


admin.site.unregister(Group)