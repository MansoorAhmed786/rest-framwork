from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models, transaction
from django.utils import timezone


class ProjectChoices:
    MANAGER = "manager"
    QA = "qa"
    DEVELOPER = "developer"
    OPEN = "open"
    REVIEW = "review"
    WORKING = "working"
    AWAITING = "awaiting_release"
    QAWAITING = "waiting_qa"
    ROLE_CHOICES = (
        (MANAGER, MANAGER),
        (QA, QA),
        (DEVELOPER, DEVELOPER),
    )

    STATUS_CHOICES = (
        (OPEN, OPEN),
        (REVIEW, REVIEW),
        (WORKING, WORKING),
        (AWAITING, AWAITING),
        (QAWAITING, QAWAITING)
    )

    @classmethod
    def get_roles(cls):
        role = []
        for i in cls.ROLE_CHOICES:
            role.append(i[0])
        return role

    @classmethod
    def get_status(cls):
        status = []
        for i in cls.STATUS_CHOICES:
            status.append(i[0])
        return status


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ProjectChoices.ROLE_CHOICES)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.email


class Project(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    team_members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return f"{self.title[:50]}...."


class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ProjectChoices.STATUS_CHOICES,
        default=ProjectChoices.OPEN
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Document(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    file = models.FileField(null=True, blank=True, upload_to='documents/')
    version = models.CharField(max_length=10, default="0.0")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author.email} on {self.created_at}'
