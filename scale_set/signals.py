from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InfoFields

@receiver(post_save, sender=InfoFields, dispatch_uid="on_login")
def on_login(sender, **kwargs):
    this_one =kwargs.get("instance")
    created=kwargs.get("created")
    print(created)
    if created:
        pass
    else:
        this_one.age=110
        print(this_one.age)