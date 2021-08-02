from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from knox import views as knox_views
urlpatterns = [
    path('documents/', views.DocumentList.as_view()),
    path('documents/<int:pk>/', views.DocumentDetail.as_view()),
    path('document-headers/', views.DocumentHeaderList.as_view()),
    path('document-headers/<int:pk>/', views.DocumentHeaderDetail.as_view()),
    path('company-document-headers/<int:pk>/',
         views.CompanyDocumentHeaderList.as_view()),
    path('company/', views.CompanyList.as_view()),
    path('company/<int:pk>/', views.CompanyDetail.as_view()),
    path('company-documents/<int:pk>/',
         views.CompanyDocumentList.as_view()),
    path('company-users/<int:pk>/',
         views.CompanyUserList.as_view()),
    path('company-waitlist/<int:pk>/', views.CompanyWaitList.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/info/', views.UserInfo.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/updatepassword/', views.UpdatePassword.as_view()),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
