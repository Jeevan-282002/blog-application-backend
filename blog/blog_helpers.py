from django.contrib.admin import action
from rest_framework import status
from rest_framework.response import Response

import constants
from blog import blog_serializers
from blog import models
from blog import blog_db_helpers
from blog.models import BlogLike, BlogPost


def get_blog_list(self, request):
    try:
        blog_data = blog_db_helpers.get_blog_data(request)
        if not blog_data:
            return Response(
                {"detail": "Data not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serialized_data = blog_serializers.BlogPostSerializer(
            blog_data, many=True, context={"request": request}
        ).data

        if not serialized_data:
            return Response(
                {"detail": "Invalid Request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK
        )

    except Exception as ex:
        return Response(
            data={"message": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_my_blog_list(self, request):
    try:
        user = request.user
        if user.is_anonymous:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        blog_data = BlogPost.objects.filter(author=user)

        if not blog_data.exists():
            return Response(
                {"detail": "No blogs found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )

        serialized_data = blog_serializers.BlogPostSerializer(
            blog_data, many=True, context={"request": request}
        ).data

        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK
        )

    except Exception as ex:
        return Response(
            data={"message": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



def add_blog(self, request):
    try:
        serializer = blog_serializers.BlogPostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            blog_obj = serializer.save()
            return Response(
                data={"message": "Blog added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as ex:
        return Response(
            {"message": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



def edit_blog(self, request):
    try:
        action_type = request.data.get("action_type", None)
        if not action_type:
            return Response(
                data = {"message": "Invalid Request."},
                status=status.HTTP_400_BAD_REQUEST)

        if action_type == constants.EDIT_BLOG:
            blog_id = request.data.get("blog_id", None)
            if not blog_id:
                return Response(
                    data = {"message": "Blog ID is required."},
                    status=status.HTTP_400_BAD_REQUEST)
            blog_instance = BlogPost.objects.filter(id=blog_id).first()
            if not blog_instance:
                return Response(
                    data={"message": "blog_data not found"},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer = blog_serializers.BlogPostSerializer(blog_instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    data = {"message": "Blog updated successfully.", "data": serializer.data},
                    status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action_type == constants.DELETE_BLOG:
            blog_id = request.data.get("blog_id", None)
            if not blog_id:
                return Response(
                    data = {"message": "Blog ID is required."},
                    status=status.HTTP_400_BAD_REQUEST)

            blog_instance = BlogPost.objects.filter(id=blog_id).first()
            if not blog_instance:
                return Response(
                    data={"message": "blog_data not found"},
                    status=status.HTTP_400_BAD_REQUEST)

            blog_instance.delete()

            return Response(
                data = {"message": "Blog deleted successfully."},
                status=status.HTTP_200_OK)

        else:
            return Response(
                data = {"message": "Invalid action type."},
                status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response(
            {"message": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def toggle_like_blog(self, request):
    try:
        blog_id = request.data.get("blog_id")
        if not blog_id:
            return Response(
                {"detail": "Blog ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        blog_data = BlogPost.objects.get(id=blog_id)
        if not blog_data:
            return Response(
                {"detail": "Blog not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        like_obj, created = BlogLike.objects.get_or_create(user=request.user, blog=blog_data)
        if not created:
            like_obj.delete()
            return Response(
                data={"message": "Blog unliked."},
                status=status.HTTP_200_OK
            )
        return Response(
            data={"message": "Blog liked."},
            status=status.HTTP_201_CREATED
        )

    except Exception as ex:
        return Response(
            data={"message": str(ex)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
