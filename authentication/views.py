import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Team
from .serializers import *

User = get_user_model()


# Create your views here.
class UserThroughRateThrottle(UserRateThrottle):
    rate = '3/minute'


class RegisterView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if User.objects.filter(email=email).exists():
            return Response({'message': 'User with this email already exists. Please log in.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        request.session['otp'] = otp
        request.session['email'] = email
        return Response({'message': 'OTP sent to email'}, status=status.HTTP_201_CREATED)

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        if email != request.session.get('email') or otp != str(request.session.get('otp')):
            return Response({'message': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=email, defaults={'email': email})

        if created:
            # Automatically log in the user
            refresh = RefreshToken.for_user(user)
            request.session['otp'] = None  # Clear the OTP from the session
            request.session['email'] = None  # Clear the email from the session
            return Response({
                'message': 'User created successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if not User.objects.filter(email=email).exists():
            return Response({'message': 'No user with this email. Please register first.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        request.session['otp'] = otp
        request.session['email'] = email
        return Response({'message': 'OTP sent to email'}, status=status.HTTP_201_CREATED)

class VerifyLoginOTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        if email != request.session.get('email') or otp != str(request.session.get('otp')):
            return Response({'message': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        request.session['otp'] = None  # Clear the OTP from the session
        request.session['email'] = None  # Clear the email from the session
        return Response({
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    

'''
Family/Team Mebers modification views
'''
class CreateTeamView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        
        if user.team:
            return Response({'message': 'You are already in a team'}, status=status.HTTP_400_BAD_REQUEST)
        
        team = Team.objects.create()
        user.team = team
        user.save()

        return Response({'message': 'Team created successfully', 'team': TeamSerializer(team).data}, status=status.HTTP_201_CREATED)
    

class InviteMemberView(generics.GenericAPIView):
    serializer_class = InviteMemberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.team:
            return Response({'message': 'You are not in a team'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(team=user.team).count() >= 6:
            return Response({'message': 'Team is full'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        invited_user = User.objects.filter(email=email).first()

        if invited_user:
            invited_user.team = user.team
            invited_user.save()
            
            return Response({'message': 'User added to team successfully'}, UserSerializer(invited_user).data, status=status.HTTP_200_OK)
        
        return Response({'message': 'User not found', 'team': TeamSerializer(user.team).data}, status=status.HTTP_400_BAD_REQUEST)    

class RemoveMemberView(generics.GenericAPIView):
    serializer_class = RemoveMemberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.team:
            return Response({'message': 'User not in a team'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        member = User.objects.filter(email=email, team=user.team).first()

        if not member:
            member.team = None
            member.save()
            return Response({'message': 'Member removed from your team'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Member not found in your team.'}, status=status.HTTP_400_BAD_REQUEST)
