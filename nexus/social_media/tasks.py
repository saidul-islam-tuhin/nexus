# Third Party Stuff
from django.conf import settings
from django.utils import timezone

# nexus Stuff
from nexus.celery import app
# Nexus Stuff
from nexus.social_media.models import Post
from nexus.social_media.services import post_to_facebook


@app.task(name='publish_posts_to_social_media')
def publish_posts_to_social_media():
    if settings.LIMIT_POSTS is True and int(settings.MAX_POSTS_AT_ONCE) > 0:
        posts = Post.objects.filter(
            is_approved=True, is_posted=False, scheduled_time__lte=timezone.now()
        )[:int(settings.MAX_POSTS_AT_ONCE)]
    else:
        posts = Post.objects.filter(
            is_approved=True, is_posted=False, scheduled_time__lte=timezone.now()
        )

    for post in posts:
        if post.posted_at == 'fb':
            post_to_facebook(post.id)
        post.is_posted = True
        post.posted_time = timezone.now()
        post.save()