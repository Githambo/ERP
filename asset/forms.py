from django import forms
from asset.models import Asset
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User

class AdditionForm(forms.ModelForm):	
	class Meta:
		model=Asset		
		fields=("__all__")
		widgets={
			'asset_description':forms.Textarea(attrs={'col':.5,'rows':1}),
			'tag_number':forms.Textarea(attrs={'col':1,'rows':1}),
			'voucher_number':forms.Textarea(attrs={'col':1,'rows':1}),
			'serial_number':forms.Textarea(attrs={'col':1,'rows':1}),
			'location':forms.Textarea(attrs={'col':1,'rows':1}),
			'date_in_service':forms.DateInput(attrs={'type':'date'}),
			}

