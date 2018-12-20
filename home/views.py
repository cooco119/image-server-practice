from models.models import Users
from models.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SignInHandler(APIView):
    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.get_fields 
            user_id_list = []
            for user in Users.objects.all():
                user_id_list.append(user.id)
            if user_id in user_id_list:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetNoticeHandler(APIView):
    def get(self, request, format=None):
        # TODO: make notice text and serialize
        return

class RegistrationHandler(APIView):
    def post(self, request, format=None):
        serializer = UsersSerializer
        # TODO: register and return response
        return 

