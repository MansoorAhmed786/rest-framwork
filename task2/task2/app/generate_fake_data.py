from faker import Faker
import random
from django.contrib.auth import get_user_model
from app.models import Project, Task, Document, Comment, Profile,ProjectChoices
from datetime import timedelta

User = get_user_model()
fake = Faker()

def create_fake_data():
    User.objects.exclude(is_superuser=True).delete()
    Project.objects.all().delete()

    Comment.objects.all().delete()
    Document.objects.all().delete()
    Task.objects.all().delete()

    users = []
    for _ in range(30):
        user = get_user_model().objects.create_user(
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        Profile.objects.create(
            user=user,
            profile_picture=None,
            role=fake.random_element(elements=["manager","QA","developer"]),
            contact_number=fake.phone_number(),
        )
        users.append(user)
        for _ in range(4):
            project = Project.objects.create(
                title=fake.word(),
                description=fake.text(),
                start_date=fake.date_this_decade(),
                end_date=fake.date_this_decade(),
            )

        projects = Project.objects.all()
        for project in projects:
            team_members = fake.random_elements(elements=users)
            project.team_members.set(team_members)
            tasks = []
            for project in projects:
                for _ in range(2):
                    task = Task.objects.create(
                        title=fake.word(),
                        description=fake.text(),
                        status=fake.random_element(elements=["open","review","working","awaiting_release","waiting_qa"]),
                        project=project,
                        assignee=fake.random_element(elements=users),
                    )
                    tasks.append(task)
                for project in projects:
                    for _ in range(1):
                        Document.objects.create(
                            name=fake.word(),
                            description=fake.text(),
                            file=None, 
                            version=fake.random_number(digits=1),
                            project=project,
                        )
                    for user in users:
                        for _ in range(1):
                            task = fake.random_element(elements=tasks)
                            project = task.project
                            Comment.objects.create(
                                text=fake.text(),
                                author=user,
                                task=task,
                                project=project,
                            )