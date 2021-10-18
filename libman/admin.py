from django.contrib import admin
from .models import Books, Student, Employer, Issue, Return,Ebook

# Register your models here.
admin.site.register(Books)
admin.site.register(Student)
admin.site.register(Employer)
admin.site.register(Issue)
admin.site.register(Return)
admin.site.register(Ebook)
