from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event,EventSlot
from .serializers import EventSerializer, EventSlotSerializer,EventListSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404


class CreateEventView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)

        # Validate slots data
        slots_data = request.data.get('slots', [])
        if not slots_data or not isinstance(slots_data, list) or len(slots_data) == 0:
            return Response({'error': 'At least one slot is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # Create the event
            event = serializer.save()

            # Debugging statement
            print(f"Event created: {event}")

            # Create slots associated with the event
            slots_data = request.data.get('slots', [])
            slots_data_list = []

            for slot_data in slots_data:
                slot_data['event'] = event.id
                slot_serializer = EventSlotSerializer(data=slot_data)
                if slot_serializer.is_valid():
                    # Instead of saving, append to the list for bulk creation after event creation
                    slots_data_list.append(slot_serializer.validated_data)
                else:
                    event.delete()
                    return Response(slot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create slots after event creation
            created_slots = EventSlot.objects.bulk_create([EventSlot(event_id=event.id, **slot_data) for slot_data in slots_data_list])

            # Retrieve the IDs of the newly created slots
            created_slot_ids = [slot.id for slot in created_slots]

            # Serialize the created slots with IDs
            slot_serializer = EventSlotSerializer(created_slots, many=True)

            return Response({
                'success': True,
                'status': 200,
                'message': 'Event successful Created',
                'event': serializer.data,
                # 'slots': slot_serializer.data,  # You might want to replace this with the actual data for slots
            }, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventListView(APIView):
    def get(self, request, format=None):
        try:
            events = Event.objects.all()
            serializer = EventListSerializer(events, many=True)
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'events': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Error fetching events: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SingleEventDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            event = get_object_or_404(Event, pk=pk)
            serializer = EventSerializer(event)
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Success',
                'event': serializer.data,
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Event not found',
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Internal Server Error: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk, format=None):
        try:
            event = get_object_or_404(Event, pk=pk)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'message': 'Event updated successfully',
                    'event': serializer.data,
                }, status=status.HTTP_200_OK)
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Event not found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Error updating event: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            event = get_object_or_404(Event, pk=pk)
            event.delete()
            return Response({
                'success': True,
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Event deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Event not found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Error deleting event: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        