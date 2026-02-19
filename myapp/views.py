from django.shortcuts import render
from myapp.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt import  tokens
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import  authenticate
from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response (serializer.data, status=status.HTTP_200_OK)



class RegisterView(APIView):
    def post(self, request):
        # Get serializer
        # IF valid, return data
        # Else, return error msg
        if request.method == 'POST':
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'You have registered successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # throttle_scope = 'login'
    throttle_classes = [ScopedRateThrottle]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user is not None:
                return Response({'message':"You are logged in."}, status=status.HTTP_200_OK)
            else:
                return Response({'message':"Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):
    def post(self, request):
        token = tokens.RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'message':'Token blacklisted successfully.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_passw = serializer.validated_data['old_password']
            new_passw = serializer.validated_data['new_password']
            if not user.check_password(old_passw):
                return Response({'error':'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_passw)
            user.save()
            return Response({'message':"Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


