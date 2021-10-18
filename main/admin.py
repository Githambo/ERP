from django.contrib import admin
from main.models import *
from corecode.models import AcademicSession,AcademicTerm
from django.forms import Textarea

# Register your models here.

admin.site.register(HomeVisit)

admin.site.register(Parent)
admin.site.register(Church)
admin.site.register(Gift)
admin.site.register(HomevisitImages)
admin.site.register(Notification)
admin.site.register(Finance1)
admin.site.register(Leave)
admin.site.register(AcademicTerm)
admin.site.register(AcademicSession)

class StudentAdmin(admin.ModelAdmin):
	formfield_overrides={
	models.TextField:{'widget':Textarea(attrs={'rows':'1','cols':'55'})}
	}

admin.site.register(Student,StudentAdmin)

