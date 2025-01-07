from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import AudioPost, Comment, Like, UserProfile, AudioFile
from .forms import AudioUploadForm, CommentForm, ProfileForm,Profile  # Assuming ProfileForm is imported
from django.contrib.auth import login as auth_login, authenticate

def home(request):
    """Render the home page with all audio posts."""
    posts = AudioPost.objects.all().order_by('-created_at')  # Fetch all audio posts
    return render(request, 'audio/home.html', {'posts': posts})


#@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('explore_podcasts')
    else:
        form = ProfileForm()
    return render(request, 'users/create_profile.html', {'form': form})

#@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

#@login_required
def like_post(request, post_id):
    """Toggle like for a specific post."""
    post = get_object_or_404(AudioPost, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use the renamed import
            return redirect('home')  # Redirect to the home page or another page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'audio/login.html')

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'audio/register.html')

#@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)  # Ensure fetching correct object
    context = {
        'profile_picture_url': user_profile.get_profile_picture_url(),
        'bio': user_profile.bio,
    }
    return render(request, 'audio/profile.html', context)

#@login_required
def upload_audio(request):
    """Allow users to upload audio files."""
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)  # Bind form with POST and FILES data
        if form.is_valid():
            audio = form.save(commit=False)  # Don't save to DB yet, to associate user
            audio.user = request.user  # Associate the audio post with the logged-in user
            audio.save()  # Save the audio post to the database
            messages.success(request, "Audio uploaded successfully!")  # Success message
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "There was an error uploading your audio.")  # Error message
    else:
        form = AudioUploadForm()  # If it's not a POST request, initialize an empty form

    return render(request, 'audio/upload_audio.html', {'form': form})

def audio_list(request):
    # Query all audio posts
    audio_posts = AudioPost.objects.all()  # You can filter based on your needs (e.g., .filter(user=request.user))

    context = {
        'audio_posts': audio_posts,  # Pass the audio posts to the template
    }

    return render(request, 'audio/audio_list.html', context)

def audio_stream(request):
    # Get sorting parameter from the URL, default is 'recent'
    sort_by = request.GET.get('sort_by', 'recent')

    if sort_by == 'likes':
        audios = AudioFile.objects.all().order_by('-likes')  # Assuming 'likes' field exists
    else:
        audios = AudioFile.objects.all().order_by('-uploaded_at')  # Most recent first

    # Pagination
    paginator = Paginator(audios, 10)  # Show 10 audio files per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'audio/audio_stream.html', {'page_obj': page_obj, 'sort_by': sort_by})

#@login_required
def toggle_like(request, audio_id):
    audio_post = get_object_or_404(AudioPost, id=audio_id)
    user = request.user

    if user in audio_post.likes.all():
        audio_post.likes.remove(user)  # Unlike the post
        liked = False
    else:
        audio_post.likes.add(user)  # Like the post
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': audio_post.likes.count()  # Corrected to count likes
    })

def audio_detail(request, audio_id):
    audio_post = get_object_or_404(AudioPost, id=audio_id)
    
    # Check if the user has liked the post
    user_has_liked = request.user in audio_post.likes.all()

    # Fetch comments with pagination
    comments = audio_post.comments.all().order_by('-created_at')
    paginator = Paginator(comments, 5)  # Paginate comments (5 per page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.audio_post = audio_post
            comment.save()
            return redirect('audio_detail', audio_id=audio_id)
    else:
        form = CommentForm()

    return render(request, 'audio/audio_detail.html', {
        'audio_post': audio_post,
        'user_has_liked': user_has_liked,  # Pass the likes status
        'page_obj': page_obj,
        'form': form
    })

#@login_required
def add_comment(request, post_id):
    """Add a comment to a post."""
    post = get_object_or_404(AudioPost, id=post_id)
    content = request.POST.get('content')
    if content:
        Comment.objects.create(audio_post=post, user=request.user, content=content)
    return redirect('home')


def search(request):
    query = request.GET.get('q')
    if query:
        results = AudioPost.objects.filter(title__icontains=query)  # Adjust filter as needed
    else:
        results = AudioPost.objects.none()
    return render(request, 'audio/search_results.html', {'results': results})
