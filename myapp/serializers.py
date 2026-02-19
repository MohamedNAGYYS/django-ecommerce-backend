from rest_framework import serializers
from myapp.models import Users
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import secrets
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','first_name','last_name','email']


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        
        password_validation.validate_password(data['password1'])
        return data
    
    def create(self, validated_data): 
        password = validated_data['password1']
        validated_data.pop('password1')
        validated_data.pop('password2')
        user = Users.objects.create_user( 
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'], 
            email=validated_data['email'], 
            password=password
        )
    
        if 'role' in validated_data:
            user.role = validated_data['role']
            user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Users
        fields = ['email', 'password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Users
        fields = ['old_password', 'new_password']



class ForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = Users
        fields = ['email']


    def validate(self, data):
        if not Users.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email not found.')
        
        return data

    
    def create_reset(self, user):
        token = secrets.token_urlsafe(30)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        reset_link = f"https://resetPassw.com/{uid}/{token}"
        return reset_link, token
    
    def send_reset_link(self, user, reset_link):
        send_mail(
            subject='Password Reset',
            message=f"Click here to change your password: {reset_link}",
            from_email=f"noreply@example.com",
            recipient_list = [user.email]
        )

    def validated_reset(self, token, stored_token, uidb64):
        user_id = force_str(urlsafe_base64_decode(uidb64))
        if token == stored_token:
            return True
        raise serializers.ValidationError('Invalid or expired token.')
    