
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Event Registration System API Documentation",
      default_version='v1',
      description="For Django Admin Panel Login Credentials Below:\n\n Phone no: admin\n Password: admin\n\n\nMamunur Rashid\nSoftware Developer (Trainee)\nRed Dot Digital || Robi Axiata Ltd\nCell: 01767213613\nEmail: mrashid.uiu.cse@gmail.com\nGithub: https://github.com/mamun464",
      
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)






urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
   path('admin/', admin.site.urls),
   path('api/user/',include('account.urls')),
   path('api/events/',include('eventApp.urls')),
   
   
]
