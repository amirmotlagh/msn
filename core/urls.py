from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('signin', views.SignInView.as_view(), name='signin'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('like-post', views.LikePostView.as_view(), name='like-post')
]
