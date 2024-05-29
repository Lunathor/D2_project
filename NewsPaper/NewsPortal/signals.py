from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import info_after_new_post
from NewsPortal.models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def subscriber_notify_new_post(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        info_after_new_post(instance.pk)
    