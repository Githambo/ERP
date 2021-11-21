from django.db import models
from django.conf import settings
from django.urls import reverse
import datetime
from django.db.models import Q,Sum,Count
from django.contrib.auth import get_user_model
import numpy as np
from django.shortcuts import render,redirect

# Create your models here.

class Student(models.Model):
	LEVEL=(
		('STD 1','STD 1'),
		('STD 2','STD 2'),
		('STD 3','STD 3'),
		('STD 4','STD 4'),
		('STD 5','STD 5'),
		('STD 6','STD 6'),
		('STD 7','STD 7'),
		('STD 8','STD 8'),
		('FORM 1','FORM 1'),
		('FORM 2','FORM 2'),
		('FORM 3','FORM 3'),
		('FORM 4','FORM 4'),
		)
	
	SPONSOR_STATUS=(
		('self_sponsored','self_sponsored'),
		('cdc_sponsored','cdc_sponsored'),
		)
	GENDER=(
		('MALE','MALE'),
		('FEMALE','FEMALE'),
		)

	reg_number=models.TextField(max_length=20,unique=True)
	first_name=models.TextField(max_length=50)
	second_name=models.TextField(max_length=50,blank=True)
	surname=models.TextField(max_length=50)
	gender=models.TextField(choices=GENDER,null=True)
	passport=models.ImageField(upload_to='student_images',blank=True)
	school=models.TextField(max_length=200)
	location=models.TextField(max_length=150)
	level=models.TextField(choices=LEVEL)
	talent=models.TextField(max_length=300,blank=True)
	date_of_dedication=models.DateField(null=True,blank=True)
	date_of_baptism=models.DateField(null=True,blank=True)
	village=models.TextField(null=True,blank=True)
	sponsor_status=models.TextField(choices=SPONSOR_STATUS,null=True,blank=True)
	date_of_birth=models.DateField(null=True,blank=True)
	teacher=models.ForeignKey(
		to=settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		null=True,
		blank=True
  
		)

	
	centre=models.TextField(null=True,default="NAMBALE CDC")

	class Meta:
		permissions=("can_only_view_teaching_student","can_only_view_teaching_student"),
		
	def get_absolute_url(self):
		return reverse('main:student-detail',kwargs={'pk':self.id})

	def __str__(self):
		return '{} {} {}'.format(self.second_name,self.surname,self.first_name)

class HomeVisit(models.Model):
	STATUS=(
		('ongoing','ongoing'),
		('completed','completed')
		)
	student=models.ForeignKey(
		to="Student",
		on_delete=models.CASCADE,
		)
	date=models.DateField()
	staff_to_visit=models.ForeignKey(
		to=settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)
	status=models.TextField(choices=STATUS ,default='ongoing')	
	report=models.TextField(null=True,max_length=500)

	def close_visit(self):
		self.status="completed"
		self.save()

	def __str__(self):
		return 'Home Visit for {} on {}'.format(self.student,self.date)

	def get_absolute_url(self):
		return reverse('main:visit-detail',kwargs={'pk':self.id})

	class Meta:
		ordering=('-date',)

def visit_directory_path(instance,filename):
	return '{}/{}'.format(instance.homevisit_id,uuid4())

class HomevisitImages(models.Model):
	image=models.ImageField(upload_to="homevisit_images")
	visit=models.ForeignKey(
		to="HomeVisit",
		on_delete=models.CASCADE
		)
	

	def get_absolute_url(self):
		return reverse('main:visit-detail',kwargs={'pk':self.id})


class Finance1(models.Model):	
	student=models.ForeignKey(
		to="Student",
		on_delete=models.CASCADE
		)
	contribution=models.IntegerField()
	date_of_contribution=models.DateField(default=datetime.date.today)
	total=models.IntegerField()
	balance=models.IntegerField()
	

	def balance(self):
		self.balance=100-self.contribution
		return self.balance

	def total(self):
		self.total=self.contribution  + self.contribution
		return self.total

	
	def __str__(self):
		return '{} with {}'.format(self.student,self.contribution) 

class Parent(models.Model):
	first_name=models.TextField(max_length=100)
	second_name=models.TextField(max_length=100)
	phone_number=models.TextField(max_length=100)
	occupation=models.TextField(max_length=50,null=True)
	kid=models.TextField(max_length=100,null=True)
	

	def __str__(self):
		return '{} {} [{}] ' .format(self.first_name,self.second_name,self.phone_number)


	def kid(self):
		ss=Student.objects.filter(parent=self.id)
		for s in ss:
			return s
	
class Church(models.Model):
	name=models.TextField(max_length=300)
	location=models.TextField(max_length=300)

	def __str__(self):
		return self.name

class Gift(models.Model):
	STATUS=(
		('not_collected','not_collected'),
		('collected','collected'),
		)
	student=models.ForeignKey(
		to="Student",
		on_delete=models.CASCADE
		)
	gift_type=models.TextField(max_length=100)
	status=models.TextField(choices=STATUS,default="not_collected")

	class Meta:
		ordering=('-id',)

	def __str__(self):
		return '{} for {}'.format(self.gift_type,self.student)




class Notification(models.Model):
	TOPIC=(
		('Abuse','Abuse'),
		('Health','Health'),
		('Location','Location')
		)
	SUB_TOPIC=(
		('sick','sick'),
		('admitted','admitted'),
		('accident','accident'),
		('raped','raped'),
		('missing','missing'),
		('assaulted','assaulted')
		)
	
	student=models.ForeignKey(
		to=Student,
		on_delete=models.CASCADE
		)
	topic=models.TextField(choices=TOPIC,null=True)
	notification_date=models.DateField(default=datetime.date.today)
	detail=models.TextField(choices=SUB_TOPIC,null=True)


	def __str__(self):
		return 'Notification for {} on {} {}'.format(self.student,self.topic,self.detail)

class Message(models.Model):
	recipient=models.ForeignKey(
		to="Parent",
		on_delete=models.CASCADE
		)
	message=models.TextField(max_length=500)

	def __str__(self):
		return 'Message to {}'.format(self.recipient)


class Leave(models.Model):	
	staff=models.ForeignKey(
		to=settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
		)
	
	status=models.TextField(max_length=50,default='not_approved')
	start_date=models.DateField(null=True)
	end_date=models.DateField(null=True)
	
	def leave_approve(self):		
		self.status='approved'
		self.save()

	def leave_reject(self):
		self.status='rejected'
		self.save()

	def leave_close(self):
		self.status='closed'
		self.save()

	def number_of_days(self):
		d=np.busday_count(self.start_date,self.end_date)		
		number_of_days_taken=d
		return number_of_days_taken

	def total_taken_days(self):		
		all_staff=get_user_model().objects.filter(leave=self)	
		for every_one in all_staff:
			item=Leave.objects.filter(Q(status='approved')|Q(status='closed')|Q(staff=every_one.id))
			for days in item:				
				days_taken = np.sum(days.number_of_days())					
				return days_taken	
		
	def remaining_days(self):		
		all_staff=get_user_model().objects.filter(leave=self)
		for every_one in all_staff:			
			items=Leave.objects.filter(Q(status='approved')|Q(status='closed')|Q(staff=every_one.id))
			for days in items:
				remaining_days=21-days.total_taken_days()							
			return remaining_days


	def __str__(self):
		return 'leave request for  {}'.format(self.staff)


	class Meta:
		permissions=("can_approve_leave","can_approve_leave"),

	def get_absolute_url(self):
		return reverse('main:leave-detail',kwargs={'pk':self.id})


class Performance(models.Model):
	EXAM_TYPE=(
			('FIRST_TERM','FIRST TERM'),
			('SECOND_TERM','SECOND TERM'),
			('THIRD_TERM','THIRD TERM'),

		)


	student=models.ForeignKey(
		to="Student",
		on_delete=models.CASCADE
		)
	exam_type=models.TextField(choices=EXAM_TYPE,null=True)
	marks=models.DecimalField(max_digits=5,decimal_places=2)
	grade=models.TextField(max_length=3)
	position=models.IntegerField()

	def __str__(self):
		return 'Performance for {}'.format(self.student)


class BulkStudentUpload(models.Model):	
	csv_file            = models.FileField(upload_to='student/bulkupload/')
