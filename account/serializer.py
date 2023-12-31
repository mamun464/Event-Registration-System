from rest_framework import serializers
from account.models import CustomUser,EventRegistration
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from account.utils import Util
from django import forms
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils import timezone

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'fullName', 'phone_no','is_staff','password', 'password2',]
        extra_kwargs = {
            'password':{'write_only':True}
        }

    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        email = (attrs.get('email')).lower()
        print('Email-From-Validation:', email)
        #validate password and confirm password is same
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"{email} with this email already exists.")
        #validate password and confirm password is same
        if(password != password2):
            raise serializers.ValidationError("Confirm password not match with password!")

        return attrs
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
        phone_no = serializers.CharField(max_length=20)
        class Meta:
            model = CustomUser
            fields = ['phone_no', 'password',]

        def validate(self, data):
            phone_no = data.get('phone_no')
            password = data.get('password')

            user = authenticate(phone_no=phone_no, password=password)

            if user is not None:
                if not user.is_active:
                    raise AuthenticationFailed('Account disabled, contact with Manager')

                # Update last_login time for the user
                user.last_login = timezone.now()
                user.save()

                # Return both the authenticated user and validated data
                return {'user': user, 'data': data}
            else:
                raise AuthenticationFailed(f'Invalid credentials, try again or Account disabled')
            

class UserListSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ['id','fullName','email','phone_no', 'user_profile_img','is_active','is_staff']

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['user', 'slot', 'registration_date']
        


