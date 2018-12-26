from models.models import Users
from models.models import Image
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

class PostImageHandler(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        
        reqData = request.reqData
        img_name = reqData.get("image_name")
        img_data = reqData.get("image_data")# TODO:보내고 받을 때에 패키지 써야할 것가틈
        user = reqData.get("user")
        isPrivate = reqData.get("is_private")
        checksum = reqData.gt("checksum")

        

        data = {
            "status": m_status,
            "msg": msg,
            "image_oid": img_oid
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')

    def uploadImage():
        minioClient = Minio('127.0.0.1:19000',
                            access_key='FM9GO6CT17O8122165HB',
                            secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
                            secure=True)