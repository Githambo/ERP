from django.urls import path
from main import views

app_name="main"


urlpatterns=[
	path('',views.index,name="index"),

	##########################    STUDENT SECTION         ###########################
	path('newstudent',views.StudentCreateView.as_view(),name="add-student"),
	path('student/<int:pk>/',views.StudentDetail.as_view(),name="student-detail"),
	path('student/<int:pk>/update',views.StudentUpdateView.as_view(),name="student-update"),
	path('students',views.StudentList.as_view(),name="students-list"),
	path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='student-delete'),




	path('visit/<int:pk>',views.VisitDetail.as_view(),name="visit-detail"),
	
	path('search',views.search,name="search"),
	
	
	path('newvisit',views.NewVisit.as_view(),name="add-homevisit"),
	path('vsearch',views.visit_search,name="visit-search"),
	path('visits',views.VisitList.as_view(),name="visit-list"),
	path('giftallocation',views.GiftAllocation.as_view(),name="gift-allocation"),
	path('giftlist',views.GiftList.as_view(),name="gift-list"),
	path('notifications',views.NotificationList.as_view(),name="not-list"),
	path('message',views.Message.as_view(),name="send-message"),
	path('send_sms',views.send_sms,name="send-sms"),	
	path('updateremarks/<int:pk>',views.UpdateRemarks.as_view(),name="update-remarks"),	
	path('visitclosed/<int:pk>',views.complete,name="visit-close"),	
	path('send_gift_notification',views.send_gift_notification,name="gift-notification"),
	path('createleave',views.LeaveCreate.as_view(),name="leave-create"),
	path('leaves',views.LeaveList.as_view(),name="leave-list"),
	path('leave/<int:pk>',views.LeaveDetail.as_view(),name="leave-detail"),
	path('leaveapprove/<int:pk>',views.approve_leave,name="leave-approve"),
	path('leavereject/<int:pk>',views.reject_leave,name="leave-reject"),
	path('leave_close/<int:pk>',views.close_leave,name="leave-close"),
	path('performance',views.PerformanceCreate.as_view(),name="performance-create"),	
	path('student/<int:pk>/performance',views.student_performance,name="student-performance"),	
	path('visit/<int:pk>/uploadimages',views.VisitImages.as_view(),name="image-upload"),
	path('parent',views.ParentList.as_view(),name="parent-list"),
	path('parent/<int:pk>',views.ParentDetail.as_view(),name="parent-detail"),
	path('parentsearch',views.parent_search,name="parent-search"),
	path('student_download',views.student_download,name="student-download"),
	path('gift/<int:pk>/update',views.UpdateStatus.as_view(),name='update-status'),
	
	path('student/gift',views.StudentGiftList.as_view(),name="student-gift-list"),
	
	
	#path('send_to',views.send_sms_to_specific,name="send-selected"),
	path('send_to',views.Message2.as_view(),name="send-selected"),
	#path('addparent',views.ParentCreate.as_view(),name='parent-create'),
	path('downloadcsv/', views.download_csv, name='download_csv'),
	path('upload/', views.StudentBulkUploadView.as_view(), name='student-upload'),



]