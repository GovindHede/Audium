from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.utils.timezone import now

class AudioPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    audio = models.FileField(upload_to='uploads/', null=True, blank=True)
    hashtag = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audio_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        related_name='liked_audio_posts',
        blank=True
    )  # Ensure related_name is unique
    
    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    audio = models.ForeignKey(AudioPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # Temporarily allow null
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.audio.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(AudioPost, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_profile_picture_url(self):
        """Returns the URL of the profile picture or a default image."""
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default_profile_picture.jpg'  # Update to the actual path of your default image


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Signal to create or update user profile automatically."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='uploads/audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # Add likes field

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        default='profile_pictures/default_profile.png'
    )

    def __str__(self):
        return self.user.username
    
class Audio(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioPost
        fields = ['title', 'description', 'audio', 'hashtag']