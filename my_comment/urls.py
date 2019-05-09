from django.urls import path
from . import views


app_name = 'comments'

urlpatterns = [
    path('<int:post_pk>/create/', views.CommentCreateView.as_view(),
         name='comment_create'),
    path('<int:post_pk>/<int:pk>/delete', views.CommentDeleteView.as_view(),
         name='comment_delete'),
]
