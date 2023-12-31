from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    date = models.DateField()
    time= models.TimeField(blank=True, null=True)
    location_name = models.CharField(max_length=255)
    

    def __str__(self):
        return f"{self.id}-{self.title}"
    
class EventSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_seat = models.PositiveIntegerField()
    occupied_seat = models.PositiveIntegerField(default=0)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')

    def __str__(self):
        return f"{self.event.title} - {self.start_time} to {self.end_time}"