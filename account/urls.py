from re import template
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views
from myshop import settings



urlpatterns = [
    path('registration/', views.sign_up, name='registration-page'),
    path('login/', views.user_login, name='login'),
    path('logout', LogoutView.as_view(
        template_name = 'account/logout.html'
    ), name='logout'),
    path('profile/', views.dashboard, name='profile'),
    path('save_bio', views.change_bio, name='bio_add'),
    path('change_prof', views.change_profile, name='change_acc'),
    path('user/<int:pk>', views.ViewProfiles.as_view(), name='user'),
    path('count', views.chng_count, name='change_nbm'),
    path('confirm/<str:code>/<int:id>',  views.confirm_pass, name='confirm'),
    path('reset_pass', views.forgot_pass, name='forgot_pass_page'),
    path('', include('social_django.urls', namespace='social')),
    path('password-change/', PasswordChangeView.as_view(
        template_name = 'account/change_pass.html'
    ), name='password_change'),
    path('password-change/done/', views.pass_chng_done, name='password_change_done'),
    path('prof_image_change', views.prof_img_change, name='img_change')
]
