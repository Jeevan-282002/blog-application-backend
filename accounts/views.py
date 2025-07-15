from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from accounts import account_helpers


class RegisterUserProfileView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        return account_helpers.do_registration(self, request)


class UserLoginView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        return account_helpers.user_login(self, request)
