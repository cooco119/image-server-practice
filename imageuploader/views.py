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
import datetime
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
# from PIL import Image as pil_Image

class UploadeHandler(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, bucketName, objectName, format=None):

        # in future, these keys should be created for user specifically
        # and users should register the service

        minioClient = Minio('127.0.0.1:9000',
                            access_key='FM9GO6CT17O8122165HB',
                            secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
                            secure=False)

        try:
            if minioClient.bucket_exists(bucketName):
                try:
                    url = minioClient.presigned_put_object(bucketName, objectName, expires=datetime.timedelta(seconds=20))
                    msg = "Successfully generated url"
                    m_status = status.HTTP_200_OK
                except ResponseError as err:
                    print(err)
                    msg = err
                    url = ""
                    m_status = status.HTTP_403_FORBIDDEN
            else:
                try:
                    minioClient.make_bucket(bucketName, location='ap-southeast-1')
                    msg = "created bucket \n"
                    try:
                        url = minioClient.presigned_put_object(bucketName, objectName, expires=datetime.timedelta(seconds=20))
                        msg += "Successfully generated url"
                        m_status = status.HTTP_200_OK
                    except ResponseError as err:
                        print(err)
                        msg += err
                        url = ""
                        m_status = status.HTTP_403_FORBIDDEN
                except ResponseError as err:
                    print(err)
                    m_status = status.HTTP_404_NOT_FOUND
                    url = ''
                    msg = ''
        except ResponseError as err:
            print(err)
            m_status = status.HTTP_404_NOT_FOUND
            url = ''
            msg = ''
        
        data = {
            "status": m_status,
            "url": url,
            "msg": msg
        }
        return Response(data=json.dumps(data), status=m_status, content_type='application/json')
    
    def post(self, request, format=None):

        ALLOWED_FORMATS = ['jpeg','jpg','png']

        reqData = request.data
        image_name = reqData.get("image_name")
        image_format = reqData.get("image_format").lower()
        bucket_name = reqData.get("image_data").get("bucketName")
        object_name = reqData.get("image_data").get("objectName")
        user = reqData.get("user")
        is_private = reqData.get("is_private")
        pub_date = reqData.get("pub_date")
        preview_url = ''

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
        try:
            # print("try inserting")
            # print(oid.objects.all().filter(bucket_name=bucket_name).filter(object_name=object_name).exists())
            if (oid.objects.all().filter(bucket_name=bucket_name).filter(object_name=object_name).exists()):
                # m_oid = oid.objects.all().filter(bucket_name=bucket_name).filter(object_name=object_name).get()
                m_status = status.HTTP_409_CONFLICT
                msg = "Image already exists"
                data = {
                    "status": m_status,
                    "msg": msg
                }
                return Response(data=json.dumps(data), 
                            status=m_status,
                            content_type='application/json')
            else:
                m_oid = oid(url='127.0.0.1', bucket_name=bucket_name, object_name=object_name)
                m_oid.save()
            # print(pub_date)
            
                m_image = Image(image_name=image_name, image_oid=m_oid, preview_url=preview_path, user=m_user, is_private=is_private, pub_date=pub_date)
                
                try:
                    m_image.save()
                except Exception as e:
                    print(e)
                print('image saved')
            
                
        except:
            m_status = status.HTTP_406_NOT_ACCEPTABLE
            msg = "Failed inserting DB"
            data = {
                "status": m_status,
                "msg": msg
            }
            return Response(data=json.dumps(data), 
                            status=m_status,
                            content_type='application/json')
        

        m_status = status.HTTP_201_CREATED
        msg = "Success"
        data = {
            "status": m_status,
            "msg": msg
        }
        return Response(data=json.dumps(data), 
                        status=m_status,
                        content_type='application/json')
        
