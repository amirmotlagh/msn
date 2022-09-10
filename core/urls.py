from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('signin', views.SignInView.as_view(), name='signin'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('like-post', views.LikePostView.as_view(), name='like-post'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('search', views.SearchView.as_view(), name='search')
]
