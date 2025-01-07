from django import forms
from .models import AudioPost, Comment,Profile

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioPost
        fields = ['title', 'description', 'audio']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3
            }),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']