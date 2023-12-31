from django.urls import path
from .views import CreateEventView,EventListView,SingleEventDetailView,EventSearchView,EventDeleteView,EventUpdateView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', SingleEventDetailView.as_view(), name='event-detail'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('search/', EventSearchView.as_view(), name='event-search'),
    
]
