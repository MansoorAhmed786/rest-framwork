from django.contrib import admin,messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm
from .models import Profile,Project,Comment,Task,Document
from django.core.management import call_command
from django.contrib.auth.models import User


User = get_user_model()
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    ordering = ("email",)
    search_fields = ["email"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_superuser"]}),
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'project', 'assignee')
    list_filter = ('status', 'project', 'assignee')
    search_fields = ('title', 'description')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'version', 'project')
    list_filter = ('version', 'project')
    search_fields = ('name', 'description')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'created_at', 'task', 'project')
    list_filter = ('created_at', 'project')
    search_fields = ('text', 'author__email', 'task__title')


admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Comment, CommentAdmin)