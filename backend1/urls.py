from django.urls import path, include
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('editorial/<slug:slug>/', views.editorial, name='editorial'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Use ckeditor URLs
    path('tutorials/', views.tutorials, name='tutorials'),
    path('press-release/<slug:slug>/', views.press_release, name='press-release'),
    path('news/<slug:slug>/', views.news, name='news'),
    path('all-news/', views.all_news, name='all_news'),
    path('all-projects/', views.all_projects, name='all_projects'),
    path('all-articles/', views.all_editorials, name='all_editorials'),
    path('course/<slug:slug>/', views.newest_course, name='newest_course'),
    path('all-courses/', views.all_courses, name='all_courses'),
    
  
]
