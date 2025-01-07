from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page to display audio posts
    path('like/<int:post_id>/', views.like_post, name='like_post'),  # Liking/unliking audio posts
    path('profile/', views.profile, name='profile'),  # User profile page
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit profile page
    path('login/', auth_views.LoginView.as_view(template_name='audio/login.html', redirect_authenticated_user=True), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Logout action
    path('register/', views.register, name='register'),  # User registration page
    path('upload/', views.upload_audio, name='upload_audio'),  # Upload audio page
    path('my-audios/', views.audio_list, name='audio_list'),  # List of all audio posts by the user
    path('stream/', views.audio_stream, name='audio_stream'),  # Streaming page (sorted by likes or recent)
    path('toggle-like/<int:audio_id>/', views.toggle_like, name='toggle_like'),  # Toggle like on audio post
    path('audio/<int:audio_id>/', views.audio_detail, name='audio_detail'),  # Detail page for a specific audio post
    path('add-comment/<int:audio_id>/', views.add_comment, name='add_comment'),  # Add comment on audio post
    path('search/', views.search, name='search'),
]
