
# from django.contrib import admin
from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from account.views import UserRegistrationView,UserLoginView,EventEnrollmentView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('event-register/', EventEnrollmentView.as_view(), name='event-register'),
    path('event-deregister/', EventEnrollmentView.as_view(), name='event-deregister'),
    
    
]
