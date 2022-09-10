from django.contrib import admin

from core.mixins import NeitherAddNorDeleteAdmin, ReadOnlyAdminMixin
from core.models import Profile, Post, LikePost, Follow


class ProfileAdmin(ReadOnlyAdminMixin, NeitherAddNorDeleteAdmin):
    pass


class PostAdmin(ReadOnlyAdminMixin, NeitherAddNorDeleteAdmin):
    pass


class LikePostAdmin(ReadOnlyAdminMixin, NeitherAddNorDeleteAdmin):
    pass


class FollowAdmin(ReadOnlyAdminMixin, NeitherAddNorDeleteAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(Follow, FollowAdmin)
