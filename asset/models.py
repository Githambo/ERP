from django.db import models
from django.conf import settings
from django.urls import reverse
import datetime

# Create your models here.
class Asset(models.Model):
	CATEGORY=(
		('COMPUTERS','COMPUTER'),
		('FURNITURES','FURNITURE'),
		('OFFICE_EQUIPMENT','OFFICE EQUIPMENT'),
		('LINK_EQUIPMENT','LINK EQUIPMENT'),
		('MUSIC','MUSIC'),
		('KITCHEN UQUIPMENT','KITCHEN EQUIPMENT'),
		('SERVERS','SERVERS'),
		)	
	STATUS=(
		('IN_USE','IN_USE'),
		('DISPOSED','DISPOSED')
		)
	
	asset_description=models.TextField(max_length=100)
	tag_number=models.TextField(unique=True,blank=True)
	voucher_number=models.TextField(blank=True)	
	serial_number=models.TextField(default='None')
	category=models.TextField(choices=CATEGORY,blank=True)
	location=models.TextField(max_length=200,blank=True)
	date_in_service=models.TextField(blank=True)
	status=models.TextField(choices=STATUS,default='IN_USE')
	
	class Meta:
		ordering=('id',)
	

	def __str__(self):
		return self.asset_description


	def get_absolute_url(self):
		return reverse('main:AssetDetail',kwargs={'pk':self.id})

class BulkAssetUpload(models.Model):	
	csv_file            = models.FileField(upload_to='asset/bulkupload/')
