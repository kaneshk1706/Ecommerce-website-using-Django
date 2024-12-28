# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.urls import reverse_lazy
from six import python_2_unicode_compatible


CATEGORY_CHOICES = (
    ('Cam', 'Camera'),
    ('Wm', 'WashingMachine'),
    ('Hea', 'Headphone'),
    ('Lap', 'Laptop'),
    ('Fan', 'Fan'),
    ('Tel', 'Television'),
    ('Mob', 'Mobiles'),
    ('Fri', 'Fridge'),
    ('Fur', 'Furniture'),
    ('Gro', 'Grocery'),
    ('sho', 'Shoes'),
)

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

def validate_number(value):
    if not str(value).isdigit():
        raise ValidationError('Please enter a valid number.')

class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='productPics',default="")
    desc = models.TextField()
    price = models.IntegerField(validators=[validate_number])
    dis_price = models.IntegerField(validators=[validate_number])
    offer = models.BooleanField(default=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    stock_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=15, default="Other")
    Address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__isnull=False), name='name_not_null'),
            models.CheckConstraint(check=models.Q(gender__isnull=False), name='gender_not_null'),
            models.CheckConstraint(check=models.Q(Address__isnull=False), name='Address_not_null'),
            models.CheckConstraint(check=models.Q(city__isnull=False), name='city_not_null'),
            models.CheckConstraint(check=models.Q(mobile__isnull=False), name='mobile_not_null'),
            models.CheckConstraint(check=models.Q(pincode__isnull=False), name='pincode_not_null'),
            models.CheckConstraint(check=models.Q(state__isnull=False), name='state_not_null'),
            models.CheckConstraint(check=models.Q(country__isnull=False), name='country_not_null'),
        ]

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.dis_price

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    ordered_date = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Accepted')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)

    def send_status_email(self):
        subject = f'Order Status Update: {self.status}'
        orders_url = 'http://127.0.0.1:8000/orders/'  # Adjust the URL accordingly

        message = f'''
            <p>Your order status has been updated to <strong>{self.status}</strong>.</p>
            <p>Order ID: {self.pk}</p>
            <p>Payment ID: {self.payment.razorpay_payment_id}</p>
            <p>Product Name: {self.product.name}</p>
            <p>Quantity: {self.quantity}</p>
            <p>Price: {self.total_cost}</p>
            <img src="{self.product.img.url}" alt="{self.product.name}" style="max-width: 200px;">
            <p>You can view your orders <a href="{orders_url}">here</a>.</p>
        '''

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.user.email
        send_mail(subject, '', from_email, [to_email], html_message=message)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = OrderPlaced.objects.get(pk=self.pk).status
            if self.status != old_status:
                self.send_status_email()
        super().save(*args, **kwargs)

    @property
    def total_cost(self):
        return self.quantity * self.product.dis_price

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews',default="")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f'Review for {self.product.name}'

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'Rating for {self.product.name}'

from django.db import models
from django.contrib.auth.models import User
from .models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class ContactMessage(models.Model):
    email = models.EmailField()
    mobile = models.IntegerField(null=True)
    message = models.TextField()
    admin_reply = models.TextField(blank=True)

    def __str__(self):
        return f"{self.email} - {self.message[:20]}"



