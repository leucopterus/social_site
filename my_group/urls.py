from django.urls import path
from . import views


app_name = 'groups'

urlpatterns = [
     path('all/', views.GroupListView.as_view(),
          name='group_list'),
     path('<int:pk>/', views.GroupDetailView.as_view(),
          name='group_detail'),
     path('<int:pk>/status-<str:status>/', views.GroupDetailView.as_view(),
          name='group_detail'),
     path('<int:pk>/<str:people>/', views.members,
          name='group_people'),
     path('<int:pk>/<str:people>/<int:user_pk>/<str:status>/', views.members,
          name='group_people'),
     path('create/', views.GroupCreateView.as_view(),
          name='group_create'),
     path('<int:pk>/delete/', views.GroupDeleteView.as_view(),
          name='delete_group'),
     path('<int:pk>/update/', views.GroupUpdateView.as_view(),
          name='update_group'),
]
