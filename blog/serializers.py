from rest_framework import serializers
from .models import BlogPost
from accounts.models import UserProfile

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ('author',)
