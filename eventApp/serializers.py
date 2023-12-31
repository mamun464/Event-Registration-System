# serializers.py
from rest_framework import serializers
from .models import Event, EventSlot

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location_name']

class EventSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSlot
        fields = ['id','start_time', 'end_time', 'total_seat', 'occupied_seat']

class EventListSerializer(serializers.ModelSerializer):
    event_slots = EventSlotSerializer(many=True, read_only=True, source='event')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location_name', 'event_slots']
