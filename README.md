# manage_external_teachers
Simple web application to manage external teachers in fenix system

## How to get this application working
- Apply the missing migrations
- Go to migrations directory and check which ones you hadn't applied yet
  `cd external_teachers/app/migrations`
- Apply the migrations:
  - In the project's root:
  - `cd external_teachers`
  - `python manage.py migrate migration_name` or simply `python manage.py migrate`
- To compile the translation files:
  - `cd app`
  - `python manage.py compilemessages`
- Create a file with the name name_service in the app folder
- `cd external_teachers/app`
- `cp name_service_template.py name_service.py`
- Write in the name_service.py file the necessary code to get the student's name by his/her ist id:
  - This code is different in different environments (development and production environments)
- Now you just need to make it run
- `cd external_teachers`
- `python manage.py runserver`
- Go to localhost:8000/professoresexternos
- Enjoy it ;)
