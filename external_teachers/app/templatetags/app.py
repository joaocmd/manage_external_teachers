
from django import template
# Internationalization
from django.utils.translation import ugettext_lazy as _

register = template.Library()

ENCODING = 'utf-8'

@register.filter(name='addcss')
def addcss(field, css):
	return field.as_widget(attrs={"class":css})

@register.filter(name='semester_tag')
def semester_tag(semester):
	result = str(semester.number) + " " + _('Semester').encode(ENCODING) + " " + str(semester.year_initial) + "/" + str(semester.year_final)
	return result
