from models.models import Users
from models.models import Image
from models.models import oid
from models.serializers import UsersSerializer
from models.serializers import ImageSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import json
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from PIL import Image

class UploadeHandler(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):

        # in future, these keys should be created for user specifically
        # and users should register the service
        url = '127.0.0.1:9000'
        access_key = 'FM9GO6CT17O8122165HB'
        secret_key = 'yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4'

        m_status = status.HTTP_200_OK
        data = {
            "status": m_status,
            "url": url,
            "keys": {
                "accessKey": access_key,
                "secretKey": secret_key
            }
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')
    
    def post(self, request, format=None):

        ALLOWED_FORMATS = ['jpeg','jpg','png']

        reqData = request.data
        image_name = reqData.get("image_name")
        image_format = reqData.get("image_format")
        bucket_name = reqData.get("image_data").get("bucketName")
        object_name = reqData.get("image_data").get("objectName")
        user = reqData.get("user")
        is_private = reqData.get("is_private")
        pub_date = reqData.get("pub_date")

        if not (image_format in ALLOWED_FORMATS):
            m_status = status.HTTP_403_FORBIDDEN
            msg = "Format not supported"
            data = {
                "status": m_status,
                "msg": msg
            }
            return Response(data=json.dumps(data), 
                            status=m_status,
                            content_type='application/json')

        
        # later, this part should be user-specific
        minioClient = Minio('127.0.0.1:9000',
                            access_key='FM9GO6CT17O8122165HB',
                            secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
                            secure=True)
        '''
        # TODO: Make Preview images to show
        '''
        preview_path = ""

        # Test if user exists
        if not(Users.objects.all().filter(name=user).exists()):
            m_status = status.HTTP_404_NOT_FOUND
            msg = "User Not Found"
            data = {
                "status": m_status,
                "msg": msg
            }
            return Response(data=json.dumps(data), 
                            status=m_status,
                            content_type='application/json')
        else:
            m_user = Users.objects.all().filter(name=user).get()

        # Save to DB
        if (oid.objects.all().filter(bucket_name=bucket_name)
                             .filter(object_name=object_name)
                             .exists()):
            m_oid = oid.objects.all().filter(bucket_name=bucket_name) \
                             .filter(object_name=object_name) \
                             .get()
        else:
            m_oid = oid('127.0.0.1', bucket_name, object_name)
            m_oid.save()
        
        Image.objects.create(image_name, m_oid, preview_path, m_user, is_private, pub_date)
        m_status = status.HTTP_201_CREATED
        msg = "Success"
        data = {
            "status": m_status,
            "msg": msg
        }
        return Response(data=json.dumps(data), 
                        status=m_status,
                        content_type='application/json')
        
