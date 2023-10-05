from django.contrib import admin, messages
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import path

from .forms import UserChangeForm, UserCreationForm
from .generate_fake_data import create_fake_data
from .models import Comment, Document, Profile, Project, Task

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
    change_list_template = 'admin/app/change_list.html'

    def changeAvailability(self, request):
        create_fake_data()
        messages.add_message(request, messages.SUCCESS,
                             'Fake Data is Inserted successfully!')
        return HttpResponseRedirect("../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "change-avalibity/",
                self.changeAvailability,
                name="change-availability",
            ),
        ]
        return custom_urls + urls

    list_display = ('__str__', 'status', 'project', 'assignee')
    list_filter = ('status', 'project', 'assignee')
    search_fields = ('title', 'description')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'version', 'project')
    list_filter = ('version', 'project')
    search_fields = ('name', 'description')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'role')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'created_at', 'task', 'project')
    list_filter = ('created_at', 'project')
    search_fields = ('text', 'author__email', 'task__title')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Comment, CommentAdmin)
