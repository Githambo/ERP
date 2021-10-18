from django.urls import path

from . import views

app_name='corecode'

urlpatterns = [
  path('', views.index_view, name='home'),
  path('site-config', views.siteconfig_view, name='configs'),
  path('current-session/', views.current_session_view, name='current-session'),

  path('year/list/', views.SessionListView.as_view(), name='sessions'),
  path('year/create/', views.SessionCreateView.as_view(), name='session-create'),
  path('year/<int:pk>/update/',
       views.SessionUpdateView.as_view(), name='session-update'),
  path('year/<int:pk>/delete/',
       views.SessionDeleteView.as_view(), name='session-delete'),

  path('month/list/', views.TermListView.as_view(), name='terms'),
  path('month/create/', views.TermCreateView.as_view(), name='term-create'),
  path('month/<int:pk>/update/',
       views.TermUpdateView.as_view(), name='term-update'),
  path('month/<int:pk>/delete/',
       views.TermDeleteView.as_view(), name='term-delete'),

  path('class/list/', views.ClassListView.as_view(), name='classes'),
  path('class/create/', views.ClassCreateView.as_view(), name='class-create'),
  path('class/<int:pk>/update/',
       views.ClassUpdateView.as_view(), name='class-update'),
  path('class/<int:pk>/delete/',
       views.ClassDeleteView.as_view(), name='class-delete'),

  path('subject/list/', views.SubjectListView.as_view(), name='subjects'),
  path('subject/create/', views.SubjectCreateView.as_view(),
       name='subject-create'),
  path('subject/<int:pk>/update/',
       views.SubjectUpdateView.as_view(), name='subject-update'),
  path('subject/<int:pk>/delete/',
       views.SubjectDeleteView.as_view(), name='subject-delete'),

  path('category/list',views.ExpenseCategoryListView.as_view(),name='category'),
  path('category/create',views.ExpenseCategoryCreateView.as_view(),name='category-create'),
  path('category/<int:pk>/update',views.ExpenseCategoryUpdateView.as_view(),name='category-update'),
  path('category/<int:pk>/delete',views.ExpenseCategoryDeleteView.as_view(),name='category-delete'),

]
