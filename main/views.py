from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum,Count
from django.http import HttpResponse
from django.forms import modelformset_factory
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy
from django.forms import widgets
from twilio.rest import Client
from twilio import *
import numpy as np



# Create your views here.
from main.models import *
from main.forms import*
from finance.models import Invoice
import csv



@login_required
def siteconfig_view(request):
  """ Site Config View """
  if request.method == 'POST' :
    form = SiteConfigForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Configurations successfully updated')
      return HttpResponseRedirect('site-config')
  else:
    form = SiteConfigForm(queryset=SiteConfig.objects.all())

  context = {"formset": form, "title": "Configuration"}
  return render(request, 'main/siteconfig.html', context)



@login_required
def index(request):
	template_name='base.html'
	notice=Notification.objects.filter(notification_date=datetime.date.today())
	number_of_notifications=notice.count()
	user_approved=Leave.objects.filter((Q(staff=request.user))&(Q(status='approved')))
	user_rejected=Leave.objects.filter((Q(staff=request.user))&(Q(status='rejected')))
	teacher_per_class=Student.objects.filter(teacher=request.user)
	teacher_per_class_count=Student.objects.filter(teacher=request.user).count()
	order_list=Leave.objects.filter(status='not_approved')
	ctc={'teacher_per_class_count':teacher_per_class_count,'teacher_per_class':teacher_per_class,'user_rejected':user_rejected,'notice':notice,'number_of_notifications':number_of_notifications,'user_approved':user_approved,'order_list':order_list}	
	return render(request,template_name,ctc)
@login_required
def search(request):
	template_name='main/search.html'
	if request.method=='GET':
		query=request.GET.get('q')
		submitbutton=request.GET.get('submit')

		if query is not None:
			results=Student.objects.filter(Q(reg_number__icontains=query)|Q(first_name__icontains=query)|Q(second_name__icontains=query))
			return render(request,template_name,{'results':results,'submitbutton':submitbutton})
		else:
			return render(request,template_name)
@login_required
def visit_search(request):
	template_name='main/visit-search.html'
	if request.method=='GET':
		query=request.GET.get('q')
		submitbutton=request.GET.get('submit')

		if query is not None:
			results=HomeVisit.objects.filter(Q(date__icontains=query)|Q(status__icontains=query))
			return render(request,template_name,{'results':results,'submitbutton':submitbutton})
		else:
			return render(request,template_name)


class StudentCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
  form_class = StudentForm
  template_name = 'main/mgt_form.html'
  success_url = reverse_lazy('student-list')
  success_message = 'Student successfully added'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Add new New Student'
      return context

class StudentDetail(LoginRequiredMixin,DetailView):
	model=Student

	def get_context_data(self, **kwargs):
		context = super(StudentDetail, self).get_context_data(**kwargs)
		context['payments'] = Invoice.objects.filter(student=self.object)
		return context
		

class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class=StudentForm
	
    success_message = "Record successfully updated."
    success_url = reverse_lazy('main:students-list')
    template_name='main/student_update.html'

    
class StudentList(LoginRequiredMixin,ListView):
	model=Student

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('main:students-list')



class VisitDetail(LoginRequiredMixin,DetailView):
	model=HomeVisit
	def visit_image_form(self):
		if self.request.user.is_authenticated:
			return HomevisitImagesForm()
		return None

	def get_parent_number(self):
		if self.request.method=='POST':
			query=request.POST.get('student')
			parent=HomeVisit.objects.filter(student=1)
			number=parent.phone_number
			return number

		

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(**kwargs)
		context['closed']=HomeVisit.objects.filter(Q(id=self.object.id)&Q(status="ongoing")&Q(staff_to_visit=self.request.user)) 
		context['image_form']=self.visit_image_form()
		context['number']=self.get_parent_number()
		return context

class VisitList(LoginRequiredMixin,ListView):
	model=HomeVisit


	
class NewStudent(LoginRequiredMixin,CreateView):
	form_class=StudentForm
	template_name='main/student-add.html'
	model=Student

	def form_valid(self,request):
		if self.request.method=='POST':
			form=StudentForm(self.request.POST,self.request.FILES)
			if form.is_valid():
				form.save()
				#return HttpResponse("Gift Saved succesfully")
			return render(request,self.template_name,{'form':form})
		else:
			form=StudentForm()
			return render(request,self.template_name)

class NewVisit(LoginRequiredMixin,CreateView):
	form_class=VisitForm
	template_name='main/homevisit-add.html'

	def form_valid(self,request):
		if self.request.method=='POST':
			form=VisitForm(self.request.POST,self.request.FILES)
			if form.is_valid():
				form.save()
				return HttpResponse("HomeVist scheduled added succesfully")
			return render(request,self.template_name,{'form':form})
		else:
			form=VisitForm()
			return render(request,self.template_name)


class VisitImages(LoginRequiredMixin,CreateView):
	form_class=HomePhotoForm
	template_name='main/update_homevisit2.html'

	def get_initial(self):
		initial=super().get_initial()
		initial['visit']=self.kwargs["pk"]
		return initial


	def form_valid(self,request):
		if self.request.method=='POST':
			form=HomePhotoForm(self.request.POST,self.request.FILES)
			if form.is_valid():
				form.save()	
				return redirect('main:visit-list')			
			return render(request,self.template_name,{'form':form})
		else:
			form=HomePhotoForm()
			return render(request,self.template_name)


	def get_context_date(self,*args,**kwargs):
		context=super().get_context_data(**kwargs)
		context['visit']=self.get_initial()
		return context

	def get_absolute_url(self):
		return reverse('main:visit-detail',kwargs={'pk':self.id})

class GiftAllocation(LoginRequiredMixin, CreateView):
    model = Gift
    fields = ['student','gift_type','status']
    success_url = reverse_lazy('main:gift-list')
    template_name='main/gift_allocation.html'

    #def get_initial(self):
    	#initial=super().get_initial()
    	#initial['student']= Student.objects.get(pk=self.request.GET.get['student'])
    	#return initial

    def form_valid(self,request):
    	if self.request.method=='POST':
    		form=GiftForm(self.request.POST)
    		if form.is_valid():
    			form.save()
    			return redirect('main:gift-list')
    		return render(request,self.template_name,{'form':form})	

    def send_sms_to_parent(self):
    	parent=Parent.objects.filter(student=student)
    	number=Parent.phone_number
    	mytwilionum="+12072227121"
    	client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    	client.messages.create(
    		to=number,
    		from_=mytwilionum,
    		body="Mzazi unaombwa uje kuchukua zawadi ya mtoto"

    		)
  
    #def get_context_data(self, **kwargs):
       # context = super(GiftAllocation, self).get_context_data(**kwargs)
        #student = Student.objects.get(pk=self.request.GET['student'])
       # context['student'] = student
       # context['student']=self.get_initial()  
        #context['form']=self.form_valid()           
        #return context


class GiftList(LoginRequiredMixin,ListView):
	model=Gift
class StudentGiftList(ListView):
	model=Student	
	template_name='main/giftallocation.html'

	def get_all(self):
		all_student=Student.objects.all()
		return all_student

	def get_context_data(self, **kwargs):
		context=super().get_context_data(**kwargs)		
		context['all_student']=self.get_all()
		return context	
	


class NotificationList(LoginRequiredMixin,ListView):
	model=Notification

class Message(LoginRequiredMixin,CreateView):
	form_class=MessageForm
	template_name='base.html'

	def get_initial(self):
		ss=Parent.objects.all()
		for everys in ss:
			return {'recipient':everys}


	def form_valid(self,request):
		if self.request.method=='POST':
			form=MessageForm(self.request.POST)
			if form.is_valid():	
				note="Message has been sent"			
				form.save()				
				return redirect("/")
			return render(request,self.template_name,{'form':form,'note':note})
		else:
			form=MessageForm()
			return render(request,self.template_name)

class Message2(LoginRequiredMixin,CreateView):
	form_class=MessageForm2
	template_name='main/message_centre.html'

	#def get_initial(self):
		#ss=Parent.objects.all()
		#for everys in ss:
			#return {'recipient':everys}


	def form_valid(self,request):
		if self.request.method=='POST':
			form=MessageForm2(self.request.POST)
			if form.is_valid():	
				note="Message has been sent"			
				form.save()				
				return redirect("/")
			return render(request,self.template_name,{'form':form,'note':note})
		else:
			form=MessageForm2()
			return render(request,self.template_name)

@login_required
def send_gift_notification(request):
	template_name='base.html'
	mytwilionum="+12072227121"
	client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)	
	allparent=Parent.objects.all()
	client.messages.create(
				to="+254704478977",
				from_=mytwilionum,
				body="Dear Parent Kindly come and Collect The Gift of your student"
				)

def send_sms_to_specific(request):
	template_name='main/message_centre.html'
	#mytwilionum="+12072227121"
	#client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)	
	#numbers=request.POST.get("numbers")
	#message=request.POST.get("message")
	#for single_number in numbers:
	#client.messages.create(
				#to="+254704478977",
				#from_=mytwilionum,
				#body="from the website"
				#)
	
	return render(request,template_name)


@login_required
def send_sms(request):
	template_name='base.html'
	mytwilionum="+12072227121"		
	if request.method=='GET':
		sms=request.GET.get('message')
		mytwilionum="+12072227121"
		client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)	
		
		client.messages.create(
				to="+254784433029",
				from_=mytwilionum,
				body=sms
				)
		#allparent=Parent.objects.all()
		#client.messages.create(
				#to="+254704478977",
				#from_=mytwilionum,
				#body=sms
				#)
		
		#for recipient in allparent:
			##recipient_num=recipient.phone_number
			#client.messages.create(
				#to=recipient_num,
				#from_=mytwilionum,
				#body="from the website"
				#)


			
	return HttpResponse("message sent!!")


class UpdateRemarks(LoginRequiredMixin,UpdateView):
	form_class=HomeRemarkForm
	template_name='main/update_homevisit.html'
	model=HomeVisit

	def get_absolute_url(self):
		return reverse('main:visit-detail',kwargs={'pk':self.id})


class UpdateStatus(LoginRequiredMixin,UpdateView):
	form_class=GiftStatusForm
	template_name='main/update_giftstatus.html'
	model=Gift
	success_url = reverse_lazy('main:gift-list')

	
@login_required
def complete(request,pk):
	close=HomeVisit.objects.get(pk=pk)
	close.close_visit()
	return redirect("/")

class HomevisitImageUpload(LoginRequiredMixin,CreateView):
	form_class=HomevisitImagesForm
	

	def get_initial(self):
		initial=super().get_initial()
		initial['visit']=self.kwargs['visit_id']
		return visit

	def render_to_response(self,context,**response_kwargs):
		visit_id=self.kwargs['visit_id']
		homevisit_detail_url=reverse('main:visit-detail',kwargs={'pk':visit_id})
		return redirect(to=homevisit_detail_url)

	def get_success_url(self):
		visit_id=self.kwargs['visit_id']
		homevisit_detail_url=reverse('main:visit-detail',kwargs={'pk':visit_id})
		return homevisit_detail_url


class LeaveCreate(LoginRequiredMixin,CreateView):
	form_class=LeaveForm
	template_name='main/leavecreate.html'
	model=Leave

	def get_initial(self):
		return {'staff':self.request.user}

	def form_valid(self,request):
		if self.request.method=='POST':
			form=LeaveForm(self.request.POST)
			if form.is_valid():								
				form.save()				
				return redirect("/")
			return render(request,self.template_name,{'form':form})
		else:
			form=LeaveForm()
			return render(request,self.template_name)

class LeaveList(LoginRequiredMixin,ListView):
	model=Leave

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(**kwargs)
		context['single_user']=Leave.objects.filter(Q(staff=self.request.user))
		return context

class LeaveDetail(LoginRequiredMixin,DetailView):
	model=Leave

	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(**kwargs)
		context['leaves']=Leave.objects.filter(Q(id=self.object.id)&(Q(status="approved")|Q(status="closed")))
		return context
@login_required
def approve_leave(request,pk):
	close=Leave.objects.get(pk=pk)
	close.leave_approve()
	return redirect("/")
@login_required
def reject_leave(request,pk):
	close=Leave.objects.get(pk=pk)
	close.leave_reject()
	return redirect("/")
@login_required
def close_leave(request,pk):
	close=Leave.objects.get(pk=pk)
	close.leave_close()
	return redirect("/")

class PerformanceCreate(LoginRequiredMixin,CreateView):
	form_class=PerformanceForm
	template_name='main/perfomance.html'

	def form_valid(self,request):
		if self.request.method=='POST':
			form=PerformanceForm(self.request.POST)
			if form.is_valid():								
				form.save()				
				return redirect("/")
			return render(request,self.template_name,{'form':form})
		else:
			form=PerformanceForm()
			return render(request,self.template_name)

@login_required
def student_performance(request,pk):
	close=Student.objects.get(pk=pk)
	s_p=Performance.objects.filter(student=close)
	template_name='main/s_performance.html'
	return render(request,template_name,{'s_p':s_p,'close':close})
@login_required


class ParentCreate(LoginRequiredMixin,CreateView):
	form_class=ParentForm
	template_name='main/parent_create.html'

	def form_valid(self,request):
		if self.request.method=='POST':
			form=ParentForm(self.request.POST)
			if form.is_valid():								
				form.save()				
				return redirect("/")
			return render(request,self.template_name,{'form':form})
		else:
			form=ParentForm()
			return render(request,self.template_name)

class ParentList(LoginRequiredMixin,ListView):
	model=Parent

	

class ParentDetail(LoginRequiredMixin,DetailView):
	model=Parent
	
	

@login_required
def parent_search(request):
	template_name='main/p_search.html'
	if request.method=='GET':
		query=request.GET.get('q')
		submitbutton=request.GET.get('submit')

		if query is not None:
			results=Parent.objects.filter(Q(first_name__icontains=query)|Q(second_name__icontains=query)|Q(phone_number__icontains=query))
			return render(request,template_name,{'results':results,'submitbutton':submitbutton})
		else:
			return render(request,template_name)

@login_required
def student_download(request):	
	response=HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachment;filename="all_students.csv"'
	report=Student.objects.all()
	writer=csv.writer(response)
	writer.writerow(['NAME','NUMBER ','GENDER','SPONSOR'])

	for rows in report:
		writer.writerow([rows,rows.reg_number,rows.gender])

	return response

class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BulkStudentUpload
    template_name = 'main/student_upload.html'
    fields = ['csv_file']
    success_url = reverse_lazy('main:students-list')
    success_message = 'Successfully uploaded Student'
@login_required

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['reg_number', 'first_name',
    	'second_name', 'surname', 'gender'
                     ])

    return response
#