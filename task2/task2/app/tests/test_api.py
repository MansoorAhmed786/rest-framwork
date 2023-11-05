from app.models import Comment, Document, Profile, Project, ProjectChoices, Task
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class APITestCase(APITestCase):
    create = "/api/create/"
    token = "/api/token/"
    refresh = "/api/token/refresh/"
    createProject = "/api/project/"
    projectList = "/api/project/"
    projectData = "/api/project/{}/"
    deleteProject = "/api/project/{}/"
    updateProject = "/api/project/{}/"
    createTask = "/api/task/"
    taskList = "/api/task/"
    taskData = "/api/task/{}/"
    deletetask = "/api/task/{}/"
    updatetask = "/api/task/{}/"
    createDocument = "/api/document/"
    documentList = "/api/document/"
    documentData = "/api/document/{}/"
    deleteDocument = "/api/document/{}/"
    updateDocument = "/api/document/{}/"
    createComment = "/api/comment/"
    commentList = "/api/comment/"
    commentData = "/api/comment/{}/"
    deleteComment = "/api/comment/{}/"
    updateComment = "/api/comment/{}/"

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@mail.com",
            first_name="test",
            last_name="user",
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.profile = Profile.objects.create(
            user=self.user,
            role=ProjectChoices.MANAGER,
        )
        self.project = Project.objects.create(
                    title="test project",
                    start_date="2024-03-03",
                    end_date="2025-01-02",
        )
        self.project.save()
        self.task = Task.objects.create(
            title='Tast Task',
            project=self.project,
            description='Test Description',
        )
        self.task.save()
        self.document = Document.objects.create(
            project=self.project
        )
        self.document.save()
        self.comment = Comment.objects.create(
            text='this is test comment',
            author=self.user,
            task=self.task,
            project=self.project,
        )
        self.comment.save()
        self.client = APIClient()

        data = {"email": self.user.email, "password": "testpassword"}
        response = self.client.post(self.token, data, format="json")
        self.token1 = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token1}")

        #############################################################
    def test_create_user(self):
        data = {
            'email': 'test@mail.com',
            'password': 'testpass',
            'first_name': 'test',
            'last_name': 'user',
            'password2': 'testpass',
            'role': 'manager'
            }
        response = self.client.post(
            self.create,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_password(self):
        data = {
            'email': 'test@mail.com',
            'password': 'testpass',
            'first_name': ' test',
            'last_name': 'user',
            'password2': 'nottest',
            'role': 'manager'
        }
        response = self.client.post(
            self.create,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_email(self):
        data = {
            'email': 'test',
            'password': 'testpass',
            'first_name': 'test',
            'last_name': 'user',
            'password2': 'testpass',
            'role': 'manager'
        }
        response = self.client.post(
            self.create,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_name(self):
        data = {
            'email': 'test@mail.com',
            'password': 'testpass',
            'password2': 'testpass',
            'role': 'manager'
        }
        response = self.client.post(
            self.create,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_role(self):
        data = {
            'email': 'test@mail.com',
            'password': 'testpass',
            'first_name': 'test',
            'last_name': 'user',
            'password2': 'testpass',
            'role': 'notchoice'
        }
        response = self.client.post(self.create, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project(self):
        data = {
            "title": "test project",
            "start_date": "2024-03-03",
            "end_date": "2025-01-02"
        }
        response = self.client.post(
            self.createProject,
            data=data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_project_requirement(self):
        data = {"title": "test project", }
        response = self.client.post(
            self.createProject,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_start_date(self):
        data = {
            "title": "test project",
            "end_date": "2025-01-02"
        }
        response = self.client.post(
            self.createProject,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_end_date(self):
        data = {
            "title": "test project",
            "start_date": "2026-03-03",
            "end_date": "2025-01-02"
            }
        response = self.client.post(
            self.createProject,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_project(self):
        response = self.client.get(self.projectList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_project(self):
        response = self.client.get(
            self.projectData.format(self.project.id),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_not_found_project(self):
        response = self.client.get(
            self.projectData.format(10000),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project(self):
        data = {
            "title": "test project update",
            "start_date": "2024-03-03",
            "end_date": "2025-01-02"
            }
        response = self.client.put(
            self.updateProject.format(self.project.id),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unavailable_update_project(self):
        data = {
            "title": "test project update",
            "start_date": "2024-03-03",
            "end_date": "2025-01-02"
            }
        response = self.client.put(
            self.updateProject.format(99999999999),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_project(self):
        response = self.client.delete(
            self.deleteProject.format(self.project.id),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_unavaiable_project(self):
        response = self.client.delete(
            self.deleteProject.format(99999999999),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #############################################################
    def test_create_task(self):
        data = {
            "title": "Test Task",
            "project": self.project.id,
            "description": "This is test task description"
            }
        response = self.client.post(self.createTask, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_project_task(self):
        data = {
            "title": "Test Task",
            "description": "This is test task description"
        }
        response = self.client.post(self.createTask, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_task(self):
        data = {
            "project": self.project.id,
            "description": "This is test task description"
        }
        response = self.client.post(self.createTask, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_unavailable_task(self):
        data = {
            "title": "Test Task",
            "project": 400,
            "description": "This is test task description"
            }
        response = self.client.post(self.createTask, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_task(self):
        response = self.client.get(self.taskList, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_task(self):
        response = self.client.get(
            self.taskData.format(self.task.id),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_task(self):
        response = self.client.get(
            self.taskData.format(999999999),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task(self):
        data = {"title": "test task update"}
        response = self.client.put(
            self.updatetask.format(self.task.id),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unabailable_update_task(self):
        data = {"title": "test task update"}
        response = self.client.put(
            self.updatetask.format(999999999999),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        response = self.client.delete(
            self.deletetask.format(self.task.id),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_already_delete_task(self):
        response = self.client.delete(
            self.deletetask.format(99999999),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #############################################################
    def test_create_document(self):
        data = {"project": self.project.id, }
        response = self.client.post(
            self.createDocument,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_document(self):
        response = self.client.get(self.documentList, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_document(self):
        response = self.client.get(
            self.documentData.format(self.document.id),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_document(self):
        response = self.client.get(
            self.documentData.format(999999999),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_document(self):
        data = {"name": "updated document"}
        response = self.client.put(
            self.updateDocument.format(self.document.id),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_unalaiable_document(self):
        data = {"name": "updated document"}
        response = self.client.put(
            self.updateDocument.format(99999999999),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_document(self):
        response = self.client.delete(
            self.deleteDocument.format(self.document.id),
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_already_delete_document(self):
        response = self.client.delete(
            self.deleteDocument.format(99999999),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self):
        data = {
            "text": "This is test Comment",
            "project": self.project.id,
            "author": self.user.id,
            "task": self.task.id,
            }
        response = self.client.post(
            self.createComment,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_task_comment(self):
        data = {
            "text": "This is test Comment",
            "project": self.project.id,
             }
        response = self.client.post(
            self.createComment,
            data=data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_not_found_comment(self):
        data = {
            "text": "This is test Comment",
            "project": 999999,
            "author": 999999,
            "task": 99999,
            }
        response = self.client.post(
            self.createComment,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_not_project_comment(self):
        data = {
            "text": "This is test Comment",
            "author": self.user.id,
            "task": self.task.id,
            }
        response = self.client.post(
            self.createComment,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_comment(self):
        response = self.client.get(self.commentList, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_comment(self):
        response = self.client.get(
            self.commentData.format(self.comment.id),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_comment(self):
        response = self.client.get(
            self.commentData.format(999999999),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment(self):
        data = {"title": "updated document"}
        response = self.client.put(
            self.updateComment.format(self.comment.id),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_anailabale_comment(self):
        data = {"title": "updated document"}
        response = self.client.put(
            self.updateComment.format(99999999999),
            data=data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        response = self.client.delete(
            self.deleteComment.format(self.comment.id),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_already_delete_comment(self):
        response = self.client.delete(
            self.deleteComment.format(99999999),
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
