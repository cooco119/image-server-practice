from models.models import Users
from models.models import Image
from models.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import json

class GetWorkspaces(APIView):
    renderer_classes = (JSONRenderer, )
    
    def get(self, request, username, format=None):
        if (Users.objects.all().filter(name=username).exists()):
            names = list(Users.objects.values_list('name', flat=True).order_by('name'))
            m_status = status.HTTP_200_OK
            msg = "Success"

        else:
            m_status = status.HTTP_404_NOT_FOUND
            names = None
            msg = "User not found"
        data = {
                "status": m_status,
                "names": names,
                "msg": msg
            }
        return Response(data=json.dumps(data), status=status.HTTP_200_OK, \
                        content_type='application/json')

class GetImageListByName(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, username, name, format=None):
        if (Users.objects.all().filter(name=username).exists()):
            if (Users.objects.all().filter(name=name).exists()):

                m_status = status.HTTP_200_OK

                if (username == name):
                    image_list = Image.objects.all().filter(user__name=name) \
                                                    .values(
                                                        'image_name', 
                                                        'preview_url',
                                                        'user__name', 
                                                        'is_private', 
                                                        'pub_date'
                                                    )
                    image_list = list(image_list)
                    msg = "Success"

                else:
                    image_list = Image.objects.all().filter(user__name=name) \
                                                    .filter(is_private=False) \
                                                    .values(
                                                        'image_name', 
                                                        'preview_url',
                                                        'user__name', 
                                                        'is_private', 
                                                        'pub_date'
                                                    )
                    image_list = list(image_list)
                    msg = "Success"
            else:
                m_status = status.HTTP_404_NOT_FOUND
                img_list = None
                msg = "Target name doesn't exist!"
                    
        else:
            m_status = status.HTTP_404_NOT_FOUND
            img_list = None
            msg = "User doesn't exist!"
        
        data = {
            "status": m_status,
            "img_list": img_list,
            "msg":msg
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')

class GetImageByImageName(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, username, name, image_name, format=None):
        if (Users.objects.all().filter(user__name=username).exists()):

            if (Image.objects.all().filter(user__name=name)
                                   .filter(image_name=image_name).exists()):

                msg = "Success"
                m_status = status.HTTP_200_OK
                img = Image.objects.all().filter(user__name=name) \
                                         .filter(image_name=image_name) \
                                         .values(
                                             'image_name', 
                                             'image_oid', 
                                             'user__name', 
                                             'is_private', 
                                             'pub_date'
                                         )
            else:
                msg = "Image Not Found"
                m_status = status.HTTP_404_NOT_FOUND
                img = None

        else:
            msg = "User Not Found"
            m_status = status.HTTP_404_NOT_FOUND
            img = None
        