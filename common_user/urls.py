from django.urls import path
from . import views

app_name = 'for_users'

urlpatterns = [
    path('login/', views.page_for_log_in, name='login_page'),
    path('logout/', views.page_for_log_out, name='logout_page'),
    path('register/', views.page_for_registeration, name='registration_page'),
    path('', views.welcome_page, name='welcome'),
]
