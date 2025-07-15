from rest_framework.views import APIView
from blog import blog_helpers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from accounts import account_helpers
from rest_framework_simplejwt.authentication import JWTAuthentication


class GetBlogsView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        return blog_helpers.get_blog_list(self, request)


class GetMyBlogList(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        return blog_helpers.get_my_blog_list(self, request)


class AddBlogView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        return blog_helpers.add_blog(self, request)


class EditBlogView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        return blog_helpers.edit_blog(self, request)


class ToggleLikeView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        return blog_helpers.toggle_like_blog(self, request)