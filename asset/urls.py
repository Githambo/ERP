from django.urls import path
from asset import views

app_name='asset'

urlpatterns=[

	path('',views.index,name='index'),
	path('addition',views.MassAddition.as_view(),name='addition'),
	path('asset/<int:pk>',views.AssetDetail.as_view(),name='AssetDetail'),
	path('list',views.AssetList.as_view(),name='asset-list')	,	
	path('search/',views.SearchView,name='search'),				
	path('download-register',views.register_download,name='download-register'),
	path('upload/', views.AssetBulkUploadView.as_view(), name='asset-upload'),
    path('downloadcsv/', views.downloadcsv, name='download-csv'),
	
	
]