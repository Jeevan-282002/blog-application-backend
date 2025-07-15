from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'mobile_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        mobile_number = validated_data.pop('mobile_number', None)
        password = validated_data.pop('password')

        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
        )
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, mobile_number=mobile_number)
        return user



class UserProfileReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'mobile_number']
