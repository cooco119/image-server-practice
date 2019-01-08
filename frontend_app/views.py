from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.serializers import Serializer
import os

class fileDispatcher(APIView):
  
  def get(self, request, filepath, format=None):

    path_prefix = os.path.join(os.getcwd(), 'frontend_app', 'deepzoom')
    fullpath = os.path.join(path_prefix, filepath)
    response = HttpResponse()
    try:
      # print(os.path.splitext(filepath))
      if os.path.splitext(filepath)[1] == ".dzi":
        with open(fullpath, 'r') as file_data:
          data = file_data.read()
          # print(fullpath)
          # print(data)
          content_type = 'text/xml'
          file_data.close()
        response = HttpResponse(content_type="application/dzi")
        response.write(data)
      else:
        with open(fullpath, 'rb') as file_data:
          data = file_data.read()
          # print(fullpath)
          # print(data)
          content_type = 'image/png'
          file_data.close()
        response = HttpResponse(content_type="image/png")
        response.write(data)

      return response
    
    except Exception as e:
      print(e)
      return Response(status=status.HTTP_406_NOT_ACCEPTABLE)