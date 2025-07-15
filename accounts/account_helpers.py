from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserProfileReadSerializer
from .models import UserProfile


def do_registration(self, request):
    user_instance = UserProfile.objects.filter(mobile_number=request.data.get("mobile_number")).first()
    if user_instance:
        return Response(
            {"detail": "User Already Exists"},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"detail": "Invalid request data."},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer.save()
    return Response(
        {"message": "User registered successfully."},
        status=status.HTTP_201_CREATED
    )




def user_login(self, request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response(
            {"detail": "Account is not fully set up."},
            status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)
    user_data = UserProfileReadSerializer(user_profile).data

    return Response(
        {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
        },
        status=status.HTTP_200_OK
    )
