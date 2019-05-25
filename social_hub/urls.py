"""social_hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# next two lines are written to download and show
# media files (companies logo, etc) on HTML files:
# allow us to say where static is and where media is
from django.conf.urls.static import static
# everything that is defined in setting.py file
from django.conf import settings
from .views import search_view

urlpatterns = [
    path('', include('common_user.urls', namespace='for_users')),
    path('post/', include('my_post.urls', namespace='posts')),
    path('comment/', include('my_comment.urls', namespace='comments')),
    path('group/', include('my_group.urls', namespace='groups')),
    path('results/', search_view, name='search'),
    path('admin/', admin.site.urls),
]
# this line is written to display media files:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
