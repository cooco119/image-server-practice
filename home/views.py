from models.models import Users
from models.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import json

class SignInHandler(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data.dict()
            name = data.get("name")
            users = Users.objects.all()
            if users.filter(name=name).exists():
                m_status = status.HTTP_200_OK
                data = {
                    "status": m_status
                }
            elif not (type(name) is str):
                m_status = status.HTTP_400_BAD_REQUEST
                data = {
                    "status": m_status
                }
            else:
                m_status = status.HTTP_404_NOT_FOUND
                data = {
                    "status": m_status
                }
        else:
            m_status = status.HTTP_400_BAD_REQUEST
            data = {
                "status": m_status
            }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')

class GetNoticeHandler(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        notice_text = "Hello world @GetNoticeHandler" ## TODO: change this into file reader nexttime
        m_status = status.HTTP_200_OK
        data = {
            "status": m_status,
            "notice": notice_text
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')

class RegistrationHandler(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        data = request.data.dict()
        name = data.get("name")
        users = Users.objects.all()
        if serializer.is_valid():
            if users.filter(name=name).exists():
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

