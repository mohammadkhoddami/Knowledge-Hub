from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name = 'register'),
    path('login/', views.UserLoginView.as_view(), name = 'login'),
    path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name = 'profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name = 'reset'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('reset/complete', views.UserPasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name = 'follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name = 'unfollow'),
    path('profile/edit', views.UserEditProfileView.as_view(), name = 'edit_profile'),
]
