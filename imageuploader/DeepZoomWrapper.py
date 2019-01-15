#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import deepzoom
from threading import Thread 
from models.models import oid, Image, Users
import requests
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import datetime
import os
import base64
import time
import logging
import shutil

# Singleton class #
class DeepZoomWrapper(object):
  __instance = None
  __imageQueue = []
  __eventListners = {}
  
  @staticmethod
  def getInstance():
    if DeepZoomWrapper.__instance == None:
      DeepZoomWrapper()
    return DeepZoomWrapper.__instance
  
  # def __init__(self):
  #   if DeepZoomWrapper.__instance != None:
  #     raise Exception("An instance is already running")
  #   else:
  #     DeepZoomWrapper.__instance = self

  def put(self, ImageDbInfo):
    self.__imageQueue.append(ImageDbInfo)

  def addToEventListner(self, imageName, callable, *args):
      self.__eventListners[imageName] = {callable: args}

  def fire(self, imageName):
    for fn, args in self.__eventListners[imageName]:
      fn(args)
  
  def imageFetcher(self, bucketName, objectName, logger):
    minioClient = Minio('192.168.0.162:9000',
                        access_key='FM9GO6CT17O8122165HB',
                        secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
                        secure=False)
    logger.debug("[ImageFetcher] Initializing paths")
    dirPath = os.path.join(os.getcwd(), 'imageuploader', 'image_tmp', 'source', os.path.splitext(objectName)[0])
    os.mkdir(dirPath)
    imagePath = os.path.join(os.getcwd(), 'imageuploader', 'image_tmp', 'source', os.path.splitext(objectName)[0], objectName )
    logger.debug("[ImageFetcher] Trying to get image data from minio server")
    imageData = None
    imageFormat = ""
    exists = False
    while not exists:
      try:
        logger.debug("[ImageFetcher] Trying to connect..")
        data = minioClient.get_object(bucketName, objectName)
      except:
        time.sleep(0.5)
        continue
      else:
        exists = True
    try:
      # os.mknod(imagePath)
      # data = minioClient.get_object(bucketNam
      logger.debug("[ImageFetcher] Image get successful.")
      logger.debug("[ImageFetcher] Start writing image file..")
      with open(imagePath, 'wb+') as file_data:    
        for d in data.stream(32*1024):
          if imageData is None:
            imageData = d.split(','.encode('utf-8'))[1]
            # print(imageData)
          else:
            imageData += d
        imageFileData = base64.b64decode(imageData)
        file_data.write(imageFileData)
        file_data.close()
        logger.debug("[ImageFetcher] Successfully wrote image file")
        return imagePath

    except ResponseError as err:
      logger.error(err)

  def imageTiler(self, imagePath, logger):
    creator = deepzoom.ImageCreator(tile_size=128, tile_overlap=2, tile_format="png",
                                image_quality=0.8, resize_filter="bicubic")
    filename = os.path.split(imagePath)[1]
    filename = os.path.splitext(filename)[0] + '.dzi'
    # res_dir = os.path.join(os.getcwd(), 'imageuploader', 'image_tmp', 'processed', os.path.splitext(objectName)[0])
    res_path = os.path.join(os.getcwd(), 'imageuploader', 'image_tmp', 'processed', os.path.splitext(filename)[0], filename)
    logger.debug("[DeepZoomWrapper] Source path: " + imagePath)
    logger.debug("[DeepZoomWrapper] Result path: " + res_path)
    logger.debug("[DeepZoomWrapper] Entering deepzoom api")
    creator.create(imagePath, res_path, logger)
    return res_path


  def updateImage(self, image, imagePath, logger):
    logger.debug("[DeepZoomWrapper] Start sending to minio server")
    minioClient = Minio('192.168.0.162:9000',
                        access_key='FM9GO6CT17O8122165HB',
                        secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
                        secure=False)
    # imageName = imagePath.split('/')
    imageName = os.path.splitext(image.image_name)[0] + '.dzi'
    image_oid = image.image_oid
    bucketName = image_oid.bucket_name
    user = image.user
    is_private = image.is_private
    pub_date = image.pub_date
    processed = True
    dataDirPath = os.path.join(os.path.split(imagePath)[0] ,os.path.splitext(os.path.split(imagePath)[1])[0]+"_files")
    

    try:
      with open(imagePath, 'rb') as file_data:
        file_stat = os.stat(imagePath)
        minioClient.put_object(bucketName, imageName, file_data, file_stat.st_size, content_type='application/dzi')
        file_data.close()

      # logger.debug("[DeepZoomWrapper] Copying to frontend/public/"+imageName+"/*")
      # shutil.copyfile(imagePath, os.path.join('/home/jaejunlee/Documents/practice/image-server-practice/frontend/public/'+os.path.splitext(imageName)[0]+'/'+imageName))
      # logger.debug("[DeepZoomWrapper] Successfully copyied to frontend/public/"+imageName+"/*")

      logger.debug("[DeepZoomWrapper] Starting upload recursively to minio server, starting from " + dataDirPath)
      self.uploadRecursively(minioClient, dataDirPath, logger, os.path.split(dataDirPath)[0], bucketName, os.path.split(dataDirPath)[1], os.path.splitext(imageName)[0])
      logger.debug("[DeepZoomWrapper] Successfully sent to minio server")

      logger.debug("[DeepZoomWrapper] Copying files to frontend/public/")
      try:
        shutil.copytree(os.path.split(dataDirPath)[0], '/code/frontend_app/deepzoom/'+bucketName+'/'+os.path.splitext(imageName)[0])
        logger.debug("[DeepZeeomWrapper] Successfully copied files")
      except Exception as e:
        logger.debug("[DeepZoomWrapper] Error occured copying files: ")
        logger.debug("[DeepZoomWrapper] " + e)
        self.__imageQueue.pop()
        
      logger.debug("[DeepZoomWrapper] Deleting temporary files")
      shutil.rmtree(os.path.split(dataDirPath)[0])
      shutil.rmtree('/code/imageuploader/image_tmp/source/' + os.path.splitext(imageName)[0])
      logger.debug("[DeepZoomWrapper] Successfully deleted temporary files")

      logger.debug("[DeepZoomWrapper] Start update db")
      # r = requests.post('http://0.0.0.0:8000/imageuploader/upload/',
      #   data={
      #     "image_name": imageName,
      #     "image_format": os.path.splitext(imageName)[1],
      #     "image_data": {
      #       "bucketName": bucketName,
      #       "objectName": imageName
      #     },
      #     "user": user.name,
      #     "is_private": is_private,
      #     "pub_date": pub_date,
      #     "processed": processed
      # }, headers={'content-type': 'application/json'})
      # if r.status_code != 200:
      #   raise ResponseError

      try:
        if (oid.objects.all().filter(bucket_name=bucketName).filter(object_name=imageName).exists()):
            raise Exception
        else:
            m_oid = oid(url='192.168.0.162:9000', bucket_name=bucketName, object_name=imageName)
            m_oid.save()
            m_user = Users.objects.all().filter(name=user).get()
            m_image = Image(image_name=imageName, image_oid=m_oid, preview_url="", user=m_user, is_private=is_private, pub_date=pub_date, processed=processed)
            m_image.save()
            
            logger.debug("[DeepZoomWrapper] Deleting original image from db")
            m_image2del = Image.objects.all().filter(image_oid__bucket_name=bucketName).filter(image_name=image.image_name).get()
            m_image2del.delete()
            logger.debug("[DeepZoomWrapper] Deleting original image from minio")
            minioClient.remove_object(bucketName, image.image_name)
            logger.debug("[DeepZoomWrapper] Successfully deleted unprocessed image")

      except Exception as e:
        logger.debug("[Exception] at DeepZoomWrapper:183 " + e)
        logger.debug("[DeepZoomWrapper] Object exists?")
        self.__imageQueue.pop()

      logger.debug("[DeepZoomWrapper] Succesfully updated db")

    except ResponseError as err:
      logger.debug("[ResponseError] at DeepZoomWrapper:190 " + err)
      self.__imageQueue.pop()
    
    return

  def uploadRecursively(self, minioClient, path, logger, baseDir, bucketName, directoryName, imageName):
    if os.path.isfile(path):
      try:
        filename = os.path.relpath(path, baseDir)
        filename = filename.replace(directoryName, imageName + "_files")
        logger.debug("[DeepZoomWrapper] Sending filename: " + filename)
        with open(path, 'rb') as file_data:
          file_stat = os.stat(path)
          minioClient.put_object(bucketName, filename, file_data, file_stat.st_size)
          logger.debug("[DeepZoomWrapper] Sent file: " + filename)
          file_data.close()
      except Exception as e:
        self.__imageQueue.pop()
        logger.debug(e)
    elif os.path.isdir(path):
      for content in os.listdir(path):
        subPath = os.path.join(path, content)
        logger.debug("[DeepZoomWrapper] Entering sub directory: " + subPath)
        self.uploadRecursively(minioClient, subPath, logger, baseDir, bucketName, directoryName, imageName)
        logger.debug("[DeepZoomWrapper] Exiting to parent directory" + os.path.split(subPath)[0])
      
          

  def handleImage(self, image, logger):
    start = time.time()
    logger.debug('[DeepZoomWrapper] Started at: '+ time.strftime("%H-%M-%S"))
    bucketName = image.image_oid.bucket_name
    objectName = image.image_name
    logger.debug("[DeepZoomWrapper] bucketName: " + bucketName + ", objectName: " + objectName)
    logger.debug("[DeepZoomWrapper] Entering imageFetcher at: " + time.strftime("%H-%M-%S"))
    imagePath = self.imageFetcher(bucketName, objectName, logger)
    logger.debug("[DeepZoomWrapper] Fetched image path: " + imagePath)
    logger.debug("[DeepZoomWrapper] Entering imageTiler at: " + time.strftime("%H-%M-%S"))
    imagePath_processed = self.imageTiler(imagePath, logger)
    elapsed = time.time() - start
    self.__imageQueue.pop()
    # logger.debug('Image handling took ' + time.strftime("%S",elapsed) + 'seconds')
    return self.updateImage(image, imagePath_processed, logger)

  
  def process(self):
    threads = {}
    for image in self.__imageQueue:
      # attatch logging module
      logger = logging.getLogger(name=image.image_name)
      logger.setLevel(logging.DEBUG)
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(message)s')
      ch.setFormatter(formatter)
      logger.addHandler(ch)

      logger.debug("Creating thread..")
      m_thread = Thread(target=self.handleImage, name=image.image_name, args=(image, logger,))
      m_thread.start()
      threads[m_thread.name] = m_thread
      # m_thread.join()
      # self.__imageQueue.pop()
    
    start = time.time()
    elapsed = time.time() - start
    while threads:
      elapsed = time.time() - start
      if (elapsed % 5 == 0):
        logger.debug("[DeepZoomWrapper] processing " + len(threads) + "images for " + elapsed + " seconds.")
      for name, thread in threads:
        if not thread.is_alive():
          imageName = thread.name
          # fire(imageName)
          threads.pop(imageName, None)