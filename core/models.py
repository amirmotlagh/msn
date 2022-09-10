import uuid

from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='نام کاربر')
    id_user = models.IntegerField()
    bio = models.TextField(max_length=1024, verbose_name='بیوگرافی', blank=True, null=True)
    profileimg = models.ImageField(upload_to='profile_images',
                                   default='blank-profile-picture.png',
                                   verbose_name='عکس کاربر')
    location = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='نام کاربر')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='نام کاربر')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پسندیدن'
        verbose_name_plural = 'پسندیدن‌ها'
        unique_together = ['post', 'user']


class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='کاربر')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 verbose_name='دنبال‌کننده', related_name='follower')

    def __str__(self):
        return f'{self.follower} دنبال کننده {self.user}'

    class Meta:
        verbose_name = 'دنبال کننده'
        verbose_name_plural = 'دنبال کنندگان'
        unique_together = ['user', 'follower']
