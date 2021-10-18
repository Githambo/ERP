from django import forms
from main.models import *
from django.contrib.auth import get_user_model

class StudentForm(forms.ModelForm):
	class Meta:
		model=Student
		fields=("__all__")
		widgets={
			'reg_number':forms.Textarea(attrs={'col':1,'rows':1}),
			'first_name':forms.Textarea(attrs={'col':1,'rows':1}),
			'second_name':forms.Textarea(attrs={'col':1,'rows':1}),
			'surname':forms.Textarea(attrs={'col':1,'rows':1}),
			'school':forms.Textarea(attrs={'col':1,'rows':1}),			
			'talent':forms.Textarea(attrs={'col':1,'rows':1}),
			'location':forms.Textarea(attrs={'col':1,'rows':1}),
			'date_of_birth':forms.DateInput(attrs={'type':'date'}),
			'date_of_baptism':forms.DateInput(attrs={'type':'date'}),
			'date_of_dedication':forms.DateInput(attrs={'type':'date'}),
			'centre':forms.Textarea(attrs={'col':1,'rows':1}),	
			'village':forms.Textarea(attrs={'col':1,'rows':1}),
			
		}


class VisitForm(forms.ModelForm):
	student=forms.ModelChoiceField( 		
		queryset=Student.objects.all(),
		
		)
	class Meta:
		model=HomeVisit
		fields=['student','date','staff_to_visit']
		widgets={
			'student':forms.Textarea(attrs={'col':1,'rows':1}),
			'date':forms.DateInput(attrs={'type':'date'}),			
		}

class GiftForm(forms.ModelForm):

	class Meta:
		model=Gift
		fields=("__all__")
		widgets={
			'gift_type':forms.Textarea(attrs={'col':1,'rows':1}),
			'student':forms.Textarea(attrs={'col':1,'rows':1}),
			}
class GiftStatusForm(forms.ModelForm):

	class Meta:
		model=Gift
		fields=['status']
	
class MessageForm(forms.ModelForm):
	recipient=forms.ModelChoiceField(
		queryset=Parent.objects.all(),
		#disabled=True,
		widget=forms.HiddenInput,
		)
	class Meta:
		model=Message
		fields=("__all__")
		widgets={
			'recipient':forms.Textarea(attrs={'col':1,'rows':1}),
			}


class MessageForm2(forms.ModelForm):
	recipient=forms.ModelChoiceField(
		queryset=Parent.objects.all(),
		#disabled=True,
		#widget=forms.HiddenInput,
		)

	class Meta:
		model=Message
		fields=("__all__")
		widgets={
			'recipient':forms.Textarea(attrs={'col':1,'rows':1}),
			}


class HomeRemarkForm(forms.ModelForm):
	class Meta:
		model=HomeVisit
		fields=['report']

class HomePhotoForm(forms.ModelForm):
	
	class Meta:
		model=HomevisitImages
		fields=['visit','image']

class HomevisitImagesForm(forms.ModelForm):
	class Meta:
		model=HomevisitImages
		fields=['image','visit']

class LeaveForm(forms.ModelForm):
	
	
	class Meta:
		model=Leave
		fields=['staff','start_date','end_date']
		#fields=("__all__")

		widgets={
			'start_date':forms.DateInput(attrs={'type':'date'}),
			'end_date':forms.DateInput(attrs={'type':'date'}),			
		}

class PerformanceForm(forms.ModelForm):
	class Meta:
		model=Performance
		fields=("__all__")
		widgets={
			'marks':forms.Textarea(attrs={'col':1,'rows':1}),
			'grade':forms.Textarea(attrs={'col':1,'rows':1}),
			'position':forms.Textarea(attrs={'col':1,'rows':1}),
			}

class ParentForm(forms.ModelForm):
	class Meta:
		model=Parent
		fields=("__all__")
		
		widgets={			
			'first_name':forms.Textarea(attrs={'col':1,'rows':1}),
			'second_name':forms.Textarea(attrs={'col':1,'rows':1}),
			'phone_number':forms.Textarea(attrs={'col':1,'rows':1}),
			'occupation':forms.Textarea(attrs={'col':1,'rows':1}),			
			}


