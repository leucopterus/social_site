from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
     path('create/', views.PostCreateView.as_view(),
          name='post_create_page'),
     path('detail/<int:pk>/', views.PostDetailView.as_view(),
          name='post_detail_page'),
     path('list/', views.PostListView.as_view(),
          name='post_list_page'),
     path('update/<int:pk>/', views.PostUpdateView.as_view(),
          name='post_update_page'),
     path('delete/<int:pk>/', views.PostDeleteView.as_view(),
          name='post_delete_page'),
]
