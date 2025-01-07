from django.contrib import admin
from .models import AudioPost, Comment, Like
from .models import UserProfile
from .models import AudioFile

admin.site.register(AudioPost)
admin.site.register(Comment)
admin.site.register(Like)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','bio')


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    search_fields = ('title', 'user__username')