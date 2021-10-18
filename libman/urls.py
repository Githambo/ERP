from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),

    path('add/book',views.BookCreateView.as_view(),name="add_book"),




    path('/add/ebook',views.EbookCreateView.as_view(),name="add_ebook"),
    url(r'^book/$', views.view_books, name='view_books'),
   
    
    url(r'^student/$', views.view_student, name='view_student'),
    url(r'^student/add/$', views.add_student, name='add_student'),
    url(r'^employer/$', views.view_employer, name='view_employer'),
   
    url(r'^employer/add/$', views.add_employer, name='add_employer'),
    #url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^issue/$', views.view_issue, name='view_issue'),
    url(r'^issue/new/$', views.new_issue, name='new_issue'),
    url(r'^return_book/$', views.return_book, name='return_book'),
    path('/ebooks',views.EbookList.as_view(),name='view_ebook')
    #url(r'^delete_book/$', views.ViewDeletePost, name='delete_book'),
    #url(r'^update_book/$', views.ViewUpdatePost.as_view(), name='update_book'),
    #url(r'^book/search/$', views.search_books, name='search_books'),
]
