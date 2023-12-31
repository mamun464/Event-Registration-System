from django.urls import path
from .views import CreateEventView,EventListView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
]
