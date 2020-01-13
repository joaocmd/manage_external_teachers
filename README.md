manage_external_teachers
========================

Simple web application to manage external teachers in fenix system

<h2>How to get this application working</h2>
- Apply the missing migrations
- Go to migrations directory and check which ones you hadn't applied yet
<code>cd external_teachers/app/migrations</code>
- Apply the migrations:
- In the project's root:
- <code>cd external_teachers</code>
- <code>python manage.py migrate migration_name</code>
- Create a file with the name name_service in the app folder
- <code>cd external_teachers/app</code>
- <code>cp name_service_template.py name_service.py</code>
- Write in the name_service.py file the necessary code to get the student's name by his/her ist id:
  - This code is different in different environments (development and production environments)
- Now you just need to make it run
- <code>cd external_teachers</code>
- <code>python manage.py runserver</code>
- Go to localhost:8000/professoresexternos
- Enjoy it ;)
