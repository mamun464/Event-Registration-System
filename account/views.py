from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserRegistrationSerializer ,UserLoginSerializer,UserListSerializer,EventRegistrationSerializer,EventRegistrationSerializer
from django.contrib.auth import login
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import EventSlot
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import transaction


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({
                'success': True,
                'status':200,
                'message': 'Registration successful',
                'new_user': serializer.data,
                 'token':token ,
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Create your views here.

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Access the authenticated user from the serializer
            user = serializer.validated_data['user']

            # Your existing logic here
            user.last_login = timezone.now()
            user.save()
            
            # Log the user in (if needed)
            login(request, user)

            # Generate token
            token = get_tokens_for_user(user)

            # Serialize user details
            user_serializer = UserListSerializer(user)

            return Response({
                'success': True,
                'status': 200,
                'message': 'Login successful',
                'token': token,
                'user': user_serializer.data,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventEnrollmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Get slot_id from URL parameters
        slot_id = request.query_params.get('slot_id')

        # Check if slot_id is provided and is a valid numeric value
        if not slot_id or not slot_id.isdigit():
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid or missing slot ID in the URL parameters.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Convert slot_id to an integer
        slot_id = int(slot_id)

        user = request.user  # Assumes that the user is authenticated via JWT token
        
        try:
            slot = get_object_or_404(EventSlot, id=slot_id)
            
        except Http404:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Event Slot Not Found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Internal Server Error: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if the user is already enrolled in the slot
        if EventRegistration.objects.filter(user=user.id, slot=slot_id).exists():
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'User is already enrolled in this slot.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with enrollment
        with transaction.atomic():
            # Increment occupied_seat by 1
            previous_occupied_seat = slot.occupied_seat
            if slot.occupied_seat + 1 > slot.total_seat:
                return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Event Slot Occupied. No available seats.',
            }, status=status.HTTP_400_BAD_REQUEST)

            slot.occupied_seat += 1
            slot.save()

            # Create EventRegistration instance
            registration = EventRegistration(user=user, slot=slot)
            registration.save()

        serializer = EventRegistrationSerializer(registration)
        return Response({
            'success': True,
            'status': status.HTTP_201_CREATED,
            'message': 'Enrollment successful',
            'available_seat': slot.total_seat - (previous_occupied_seat+1),
            'enrollment': serializer.data,
        }, status=status.HTTP_201_CREATED)
    

class EventDeregistration(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, format=None):
        # Get slot_id from URL parameters
        slot_id = request.query_params.get('slot_id')

        # Check if slot_id is provided and is a valid numeric value
        if not slot_id or not slot_id.isdigit():
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid or missing slot ID in the URL parameters.',
            }, status=status.HTTP_400_BAD_REQUEST)

        # Convert slot_id to an integer
        slot_id = int(slot_id)



        user = request.user
        
        try:
            slot = get_object_or_404(EventSlot, id=slot_id)
            
        except Http404:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Event Slot Not Found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Internal Server Error: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if the user is already enrolled in the slot
        
        existing_enrollment = EventRegistration.objects.filter(user=user, slot=slot).first()

        if existing_enrollment:
            # If user is already enrolled, delete the registration (deregister)
            existing_enrollment.delete()

            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Deregistration successful',
            }, status=status.HTTP_200_OK)
        else:
            # If user is not already enrolled, return a message indicating that the user is not enrolled
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'User is not enrolled in this slot.',
            }, status=status.HTTP_400_BAD_REQUEST)
        

from .models import EventRegistration
class UserEvents(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        try:
            user = request.user

            # Retrieve the user's registrations
            user_registrations = EventRegistration.objects.filter(user=user)

            # Serialize the EventSlot objects related to the user's registrations
            serializer = EventRegistrationSerializer(user_registrations, many=True)

            # Return the response
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'retrieved Event successfully',
                'Enrolled Events': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle the case where an error occurs during serialization
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': f'Error retrieving user registrations: {str(e)}',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        