from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, Owner, Dealer

def update_user_details(instance, created=False):
    try:
        if instance.first_name:  
            instance.user.first_name = instance.first_name
        if instance.last_name:  
            instance.user.last_name = instance.last_name
        if instance.email: 
            instance.user.email = instance.email
        if created:
            if isinstance(instance, Employee):
                instance.user.is_staff = True
            elif isinstance(instance, Owner):
                instance.user.is_superuser = True
            else:
                instance.user.is_active = True
        instance.user.save()
    except Exception as e:
        print(f"Error updating user details: {e}")
        
@receiver(post_save, sender=Employee)
def create_or_update_employee_user(sender, instance, created, **kwargs):
    update_user_details(instance, created)

@receiver(post_save, sender=Owner)
def create_or_update_owner_user(sender, instance, created, **kwargs):
    update_user_details(instance, created)

@receiver(post_save, sender=Dealer)
def create_or_update_dealer_user(sender, instance, created, **kwargs):
    update_user_details(instance, created)