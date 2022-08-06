from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef, F
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import Profile, Post, LikePost


@login_required(login_url='signin')
def index(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all().annotate(profile_pic=Subquery(Profile.objects.filter(
        user_id=OuterRef('user_id')).values('profileimg')[:1]))
    return render(request, 'index.html', {'profile': profile, 'posts': posts})


class SignUpView(APIView):

    def validate_signup(self, request, username, password, password_confirmation, email):
        if password is None or password_confirmation is None:
            messages.warning(request, 'password should be filled')
        if password != password_confirmation:
            messages.warning(request, 'Password Mismatch')
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already Taken')
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username Already Taken')

    def get(self, request, **kwargs):
        return render(request, 'signup.html')

    def post(self, request, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        self.validate_signup(request, username, password, password_confirmation, email)
        if len(messages.get_messages(request)) > 0:
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        Profile.objects.create(user=user, id_user=user.id)
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)
        messages.info(request, 'Profile was created Successfully')
        return redirect('settings')


class SignInView(APIView):

    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        messages.info(request, "Credentials Invalid")
        return redirect('signin')


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth.logout(request)
        return redirect('signin')

    def permission_denied(self, request, message=None, code=None):
        return redirect('signin')


class SettingsView(APIView):

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('signin')
        try:
            profile = Profile.objects.get(user=request.user)
            return render(request, 'setting.html', {'profile': profile})
        except Exception:
            auth.logout(request)
            messages.info(request, "Profile Not Found")
            return redirect('signin')

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        user = request.user
        profile.location = request.data.get('location')
        profile.bio = request.data.get('bio')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        if request.FILES.get('image') is not None:
            profile.profileimg = request.FILES.get('image')
        profile.save()
        user.save()
        return redirect('settings')


class UploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return redirect('/')

    def permission_denied(self, request, message=None, code=None):
        auth.logout(request)
        return redirect('signin')

    def post(self, request):
        image = request.data.get('image_upload')
        caption = request.data.get('caption')

        Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('/')


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        post_id = request.GET.get('post_id')

        post = Post.objects.filter(id=post_id).first()
        if not post:
            messages.info(request, 'Post Not Found')
            return redirect('/')
        is_liked = LikePost.objects.filter(user=user, post_id=post_id).first()
        if is_liked:
            is_liked.delete()
            post.likes_count = F('likes_count') - 1
            post.save(update_fields=['likes_count'])
            return redirect('/')
        else:
            LikePost.objects.create(user=user, post_id=post_id)
            post.likes_count = F('likes_count') + 1
            post.save(update_fields=['likes_count'])
            return redirect('/')

    def permission_denied(self, request, message=None, code=None):
        auth.logout(request)
        return redirect('signin')
