from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Document, Profile, Project, Task

User = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword"))


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword"
        )
        self.profile = Profile.objects.create(user=self.user, role="manager")

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.role, "manager")


class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            start_date="2023-01-01",
            end_date="2023-02-01"
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.description, "Test Description")


class TaskModelTestCase(TestCase):
    def setUp(self):
        project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            start_date="2023-01-01",
            end_date="2023-02-01"
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Task Description",
            status="open",
            project=project
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.status, "open")


class DocumentModelTestCase(TestCase):
    def setUp(self):
        project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            start_date="2023-01-01",
            end_date="2023-02-01"
        )
        self.document = Document.objects.create(
            name="Test Document",
            description="Test Document Description",
            version="1.0",
            project=project
        )

    def test_document_creation(self):
        self.assertEqual(self.document.name, "Test Document")
        self.assertEqual(self.document.version, "1.0")
