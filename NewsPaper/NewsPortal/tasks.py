import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper import settings
from .models import Post, Subscriber


@shared_task
def info_after_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    title = post.title
    subscriber_emails = []
    
    for category in categories:
        subscriber_emails += list(Subscriber.objects.filter(category=category).values_list('user__email', flat=True))
    
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=set(subscriber_emails),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = Subscriber.objects.filter(category__name__in=categories)
    
    for sub in subscribers:
        html_content = render_to_string(
            'weekly_posts.html',
            {
                'link': 'http://127.0.0.1:8000/',
                'posts': posts,
                'user': sub.user.username
            }
        )
        msg = EmailMultiAlternatives(
            subject='Посты за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
