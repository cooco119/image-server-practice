from models.models import Users
from models.models import Image
from models.models import oid
from models.serializers import UsersSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import json
import logging

from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import datetime

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
        return Response(data=json.dumps(data), status=m_status, \
                        content_type='application/json')

class GetImageListByName(APIView):
    renderer_classes = (JSONRenderer, )
    logger = logging.getLogger(__name__)

    def get(self, request, username, targetname, format=None):
        if (Users.objects.all().filter(name=username).exists()):
            # print('p1')
            if (Users.objects.all().filter(name=targetname).exists()):
                # print('p2')
                m_status = status.HTTP_200_OK
                if (username == targetname):
                    # print('p3')
                    image_list = Image.objects.all().filter(user__name=targetname).values('image_name', 'image_oid__bucket_name', 'preview_url', 'user__name', 'is_private', 'pub_date', 'processed')
                    image_list = list(image_list)
                    for i in range(len(image_list)):
                        image_list[i]['pub_date'] = str(image_list[i].get('pub_date'))
                    # print(targetname)
                    # print(image_list)
                    msg = "Success"

                else:
                    image_list = Image.objects.all().filter(user__name=targetname).filter(is_private=False).values('image_name', 'image_oid__bucket_name', 'preview_url', 'user__name', 'is_private', 'pub_date', 'processed')
                    image_list = list(image_list)
                    for i in range(len(image_list)):
                        # print(image_list[i])
                        image_list[i]['pub_date'] = str(image_list[i].get('pub_date'))
                    msg = "Success"
            else:
                m_status = status.HTTP_404_NOT_FOUND
                image_list = None
                msg = "Target name doesn't exist!"
        else:
            m_status = status.HTTP_404_NOT_FOUND
            image_list = None
            msg = "User doesn't exist!"
        data = {
            "status": m_status,
            "img_list": image_list,
            "msg":msg
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')
        
class GetPresignedImageGetUrl(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, bucketName, objectName, format=None):

        if (oid.objects.all().filter(bucket_name=bucketName).filter(object_name=objectName).exists()):
            minioClient = Minio('192.168.0.162:9000',
                            access_key='FM9GO6CT17O8122165HB',
                            secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
                            secure=False)
            try:
                url = minioClient.presigned_get_object(bucketName, objectName,expires=datetime.timedelta(minutes=1))
                msg = "Success"
                m_status = status.HTTP_200_OK
            except ResponseError as err:
                msg = err
                url = None
                m_status = status.HTTP_403_FORBIDDEN
            data = {
                "status": m_status,
                "url": url,
                "msg":msg
            }
            return Response(data=json.dumps(data), status=m_status, content_type='application/json')
