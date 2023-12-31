from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserRegistrationSerializer ,UserLoginSerializer,UserListSerializer #,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordRestSerializer,UserProfileEditSerializer, ChangeManagerSerializer,AllUserListSerializer
from django.contrib.auth import authenticate,login
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from account.models import CustomUser
from rest_framework.renderers import JSONRenderer
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import ProtectedError
from django.contrib.auth import logout
import requests


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

