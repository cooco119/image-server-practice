from models.models import Users
from models.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import json

class SignInHandler(APIView):
    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.get_fields 
            user_id_list = []
            for user in Users.objects.all():
                user_id_list.append(user.id)
            if user_id in user_id_list:
                m_status = status.HTTP_200_OK
                data = {
                    "status": m_status
                }
                return Response(data=json.dumps(data), status=m_status, content_type='application/json')
            else:
                m_status = status.HTTP_404_NOT_FOUND
                data = {
                    "status": m_status
                }
                return Response(data=json.dumps(data), status=m_status, content_type='application/json')
        m_status = status.HTTP_400_BAD_REQUEST
        data = {
            "status": m_status
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')

class GetNoticeHandler(APIView):
    def get(self, request, format=None):
        notice_text = "Hello world @GetNoticeHandler" ## TODO: change this into file reader nexttime
        m_status = status.HTTP_200_OK
        data = {
            "status": m_status,
            "notice": notice_text
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')

class RegistrationHandler(APIView):
    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        requestData = json.loads(request.data)
        user_id = requestData.user_id
        users = Users.objects.all()
        if serializer.is_valid():
            if users.filter(name=user_id).exists():
               m_status = status.HTTP_409_CONFLICT
               data = {
                   "status": m_status
               }
               return Response(data=json.dumps(data), status=m_status)
            else:
                serializer.save()
                m_status = status.HTTP_201_CREATED
                data = {
                    "status": m_status
                }
                return Response(data=json.dumps(data), status=status.HTTP_201_CREATED)
        m_status = status.HTTP_400_BAD_REQUEST
        data = {
            "status": m_status
        }
        return Response(data=json.dumps(data), status=m_status)

