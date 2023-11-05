# Rest FrameWork

# Description

## Custom User
- Made Custom User
- User will login using email
- When a user is created must have first_name, last
-name and its role
- When a user is created it will automatically create a Profile
- Profile
- Profile is automatically created when a user is created
- Each profile have its Role
- Roles can be only manager, qa and developer
- Each role have Different Access
## Project
- Project must have its title, start_date, end_date
- End_date can't be prior than start_date
- Only manager can create a project
- Only manager can update project details
- Only manager can delete a project
- Manager can see all projects
- Assignee of these project's task can see project

## Task
- Title, description, status, project_id and user_id is compulsory
- Project_id must exist
- user_id must exist
- Status can be open, review, working, awaiting_release, waiting_qa
- A user can have many tasks
- There can be more than one tasks in a project
- Only manager can create a task
- Only manager can update a task
- Manager can see all tasks
- Tasks assignee can only see its releated tasks
- Any Task can be retieved by manager
- if its not manager and user is not an assignee of this task, that can't be accessed

## Document
- Document text, project_id and task_id is required
- Project_id and task_id must exist
- Manager can create any document
- Assignee can only create iuts relivent document
- Manager can Updata any document
- Assignee can only update its assigned task's documents
- Manager can get list of all documents
- Assignee will only get list of its assigned documents
- Manager can retieve any document
- If user is not its assignee it can't retieve it
- Only manager can delete a document

## Comment
- Text, project_id and task_id is required
- project_id and task_id m,ust exist
- Manager can create,update and delete
- Assignee can only create, update its relevent comment

##

### Apply migrations

After downloading the project you have to make migrate by using the following commands

    $ python manage.py migrate

##
### Create SuperUser

Creating a superuser account in the backend is useful so you have access to
Django Admin that will be accesible at [http://localhost:8000/admin](http://localhost:8000/admin)

To create a superuser use the following commands:

    $ python manage.py createsuperuser

##

## Run Project
To run the project use the dollowing command

    $ python manage.py runserver
##

## Getting access token
- For getting access token we use __post__ method and give email and passowrd as arguments and use /api/token/ http://localhost:8000/api/token/
- For getting refresh access token we use __post__ method and give email and passowrd as arguments and use
api/ token/refresh/ http://localhost:8000/api/token/refresh/

## Project api
- For creatng project we use __post__ method and give project title, starting and ending date and use /api/project/ http://localhost:8000/api/project/

- For updating project we give project id as argument and use __put__ method and give data which we want to update and use /api/project/{} http://localhost:8000/api/project/{}/

- For deleting project we will use  __delete__ method and give project_id as argument and we use /api/projject/{}/  http://localhost:8000/api/project/{}/

- For getting list we use __get__ method and use /api/project/ and url http://localhost:8000/api/project/

- For retreiving data we use __get__ method and pass project_id as argument we use /api/project/{}/ http://localhost:8000/api/project/{}/


## Task API
- For creating a task, use the __POST__ method and provide the task title, project ID, and description. Use /api/task/ http://localhost:8000/api/task/.

- To update a task, use the __PUT__ method and provide the task ID as an argument. Give the data you want to update and use /api/task/{}/ http://localhost:8000/api/task/{}/.

- To delete a task, use the __DELETE__ method and provide the task ID as an argument. Use /api/task/{}/ http://localhost:8000/api/task/{}/.

- To get a list of tasks, use the __GET__ method and use /api/task/ http://localhost:8000/api/task/.

- To retrieve task data, use the __GET__ method and pass the task ID as an argument. Use /api/task/{}/ http://localhost:8000/api/task/{}/.

## Document API
- For creating a document, use the __POST__ method and provide the project ID. Use /api/document/ http://localhost:8000/api/document/.

- To get a list of documents, use the __GET__ method and use /api/document/ http://localhost:8000/api/document/.

- To retrieve document data, use the __GET__ method and pass the document ID as an argument. Use /api/document/{}/ http://localhost:8000/api/document/{}/.

- To update a document, use the __PUT__ method and provide the document ID as an argument. Give the data you want to update and use /api/document/{}/ http://localhost:8000/api/document/{}/.

- To delete a document, use the __DELETE__ method and provide the document ID as an argument. Use /api/document/{}/ http://localhost:8000/api/document/{}/.

## Comment API
- For creating a comment, use the __POST__ method and provide the text, project ID, author ID, and task ID. Use /api/comment/ http://localhost:8000/api/comment/.

- To get a list of comments, use the __GET__ method and use /api/comment/ http://localhost:8000/api/comment/.

- To retrieve comment data, use the __GET__ method and pass the comment ID as an argument. Use /api/comment/{}/ http://localhost:8000/api/comment/{}/.

- To update a comment, use the __PUT__ method and provide the comment ID as an argument. Give the data you want to update and use /api/comment/{}/ http://localhost:8000/api/comment/{}/.

- To delete a comment, use the __DELETE__ method and provide the comment ID as an argument. Use /api/comment/{}/ http://localhost:8000/api/comment/{}/.