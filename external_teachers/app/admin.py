from django.contrib import admin
from .models import Profile, ExternalTeacher, Semester

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
  pass

class ExternalTeacherAdmin(admin.ModelAdmin):
  pass

class SemesterAdmin(admin.ModelAdmin):
  pass

#register admin classes
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ExternalTeacher, ExternalTeacherAdmin)
admin.site.register(Semester, SemesterAdmin)
