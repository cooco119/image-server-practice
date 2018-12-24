from models.models import Users
from models.models import Image
from models.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import json


class GetImageHandler(APIView):
    renderer_classes = (JSONRenderer, )
    
    def get(self,request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        reqData = request.data
        name = reqData.get("name")
        images = Image.objects.filter(is_private=False).values() | Image.objects.filter(is_private=True).filter(user__name=name).values()
        image_list = [image for image in images]
        m_status = status.HTTP_200_OK
        data = {
            "status": m_status,
            "image_list": image_list
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')