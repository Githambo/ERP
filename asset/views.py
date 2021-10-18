from django.shortcuts import render,redirect
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView,ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

from asset.forms import AdditionForm
from asset.models import Asset,BulkAssetUpload
import csv


def index(request):
	template_name='base.html'
	return render(request,template_name)

class AssetDetail(LoginRequiredMixin,DetailView):
	model=Asset

class MassAddition(LoginRequiredMixin,CreateView):
	form_class=AdditionForm
	template_name='asset/addition.html'
	
	def form_valid(self,request):		

		if self.request.method=='POST':
			form=AdditionForm(self.request.POST)
			if form.is_valid():
				form.save()
				return redirect('/asset-list')
		else:
			form=AdditionForm()
		return render(request,self.template_name,{'form':form})

class AssetList(LoginRequiredMixin,ListView):
	template_name='asset/asset_list.html'
	model=Asset

@login_required
def SearchView(request):
	template_name='asset/asset_search.html'
	if request.method =='GET':
		query=request.GET.get('q')
		submitbutton=request.GET.get('submit')

		if query is not None:
			results=Asset.objects.filter(Q(tag_number__icontains=query)|Q(asset_description__icontains=query))
			return render(request,template_name,{'results':results,'submitbutton':submitbutton}) 		 	
		else:
			return render(request,template_name)
	else:
		return render(request,template_name)



@login_required
def register_download(request):
	response=HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachment;filename="asset_register.csv"'
	query=Asset.objects.all()

	writer=csv.writer(response)
	writer.writerow(['DESCRIPTION','CATEGORY','TAG NUMBER','SERIAL NUMBER','LOCATION','DATE_IN_SERVICE'])
	
	for rows in query:
		writer.writerow([rows.asset_description,rows.tag_number,rows.serial_number,rows.location,rows.date_in_service])
	

	return response
class AssetBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BulkAssetUpload
    template_name = 'asset/asset_upload.html'
    fields = ['csv_file']
    success_url = reverse_lazy('asset:asset-list')
    success_message = 'Successfully uploaded Assets'


@login_required
def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asset_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['asset_description', 'tag_number',
    	'voucher_number', 'serial_number', 'category', 'location', 'date_in_service'
                     ])

    return response
#