from django.contrib import admin
from .models import Event, EventSlot

class EventSlotInline(admin.TabularInline):
    model = EventSlot
    extra = 1

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title','description', 'date','time', 'location_name')
    inlines = [EventSlotInline]

class EventSlotAdmin(admin.ModelAdmin):
    list_display = ('id','event', 'start_time', 'end_time', 'total_seat', 'occupied_seat')
    list_filter = ('event', 'start_time', 'end_time')
    search_fields = ['event__title']

admin.site.register(Event, EventAdmin)
admin.site.register(EventSlot, EventSlotAdmin)
