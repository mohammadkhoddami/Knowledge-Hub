from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'home'),
    path('post/<int:post_id>/<slug:post_slug>/', views.PostView.as_view(), name = 'post'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name = 'delete'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name = 'update'),
    path('post/create/', views.PostCreateView.as_view(), name = 'create'),
    path('reply/<int:post_id>/<int:comment_id>/', views.CommentReplyView.as_view(), name = 'reply'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name = 'like'),
]
