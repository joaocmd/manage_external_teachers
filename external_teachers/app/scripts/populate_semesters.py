# Script to create the semesters

from app.models import Semester

# Create more N semesters
N = 20

semester = Semester.get_or_create_current()
new_semester = semester

for i in range(0, N):
  new_semester = new_semester.get_or_create_next()
  print('Created new semester ' + new_semester.get_display())
