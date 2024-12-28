# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, **kwargs):
    if instance.status_changed:
        subject = f'Order {instance.order_number} Status Update'
        message = f'The status of your order {instance.order_number} has been updated to {instance.status}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.customer.email]

        send_mail(subject, message, from_email, recipient_list)
