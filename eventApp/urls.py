from django.urls import path
from .views import CreateEventView,EventListView,SingleEventDetailView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', SingleEventDetailView.as_view(), name='event-detail'),
]
