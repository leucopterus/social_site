from django.contrib import admin
from mediumeditor.admin import MediumEditorAdmin
from .models import Post
# Register your models here.


@admin.register(Post)
class PostAdmin(MediumEditorAdmin, admin.ModelAdmin):
    mediumeditor_fields = ('text', )

# admin.site.register(Post)
