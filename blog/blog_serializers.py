from rest_framework import serializers

from blog import models


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.first_name", read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = models.BlogPost
        fields = ["id", "author", "author_name", "title", "content", "created_at", "updated_at", "like_count", "is_liked"]
        read_only_fields = ["author"]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data["author"] = user
        return super().create(validated_data)
