from django.urls import path
from . import views

app_name = 'for_users'

urlpatterns = [
    path('', views.welcome_page,
         name='welcome'),
    path('login/', views.page_for_log_in,
         name='login_page'),
    path('logout/', views.page_for_log_out,
         name='logout_page'),
    path('register/', views.page_for_registeration,
         name='registration_page'),
    path('user/<int:pk>/', views.CommonUserDetailView.as_view(),
         name='user_home_page'),
    path('user/update/<int:pk>/', views.CommonUserUpdateView.as_view(),
         name='user_update_page'),
    path('user/delete/<int:pk>/', views.CommonUserDeleteView.as_view(),
         name='user_delete_page'),
]
