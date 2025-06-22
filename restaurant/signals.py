from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created:
        if instance.status == "approved":
            print(f"📢 {instance.user.name}, sizning buyurtmangiz tasdiqlandi!")
        elif instance.status == "rejected":
            print(f"❌ {instance.user.name}, afsuski, buyurtmangiz rad etildi.")
