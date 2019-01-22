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
import openslide
from openslide import deepzoom


# Singleton class #
class DeepZoomWrapper(object):
    __instance = None
    __imageQueue = []
    __eventListners = {}

    @staticmethod
    def getInstance():

        if DeepZoomWrapper.__instance is None:
            DeepZoomWrapper()

        return DeepZoomWrapper.__instance

    def put(self, ImageDbInfo):

        self.__imageQueue.append(ImageDbInfo)

    def addToEventListner(self, imageName, callable, *args):

            self.__eventListners[imageName] = {callable: args}

    def fire(self, imageName):

        for fn, args in self.__eventListners[imageName]:
            fn(args)

    def imageFetcher(self, bucketName, objectName, logger):

        minioClient = Minio(
            '192.168.0.162:9000',
            access_key='FM9GO6CT17O8122165HB',
            secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
            secure=False
        )

        logger.debug("Initializing paths")
        dirPath = os.path.join(os.getcwd(),
                               'imageuploader',
                               'image_tmp',
                               'source',
                               os.path.splitext(objectName)[0])
        os.mkdir(dirPath)
        imagePath = os.path.join(os.getcwd(),
                                 'imageuploader',
                                 'image_tmp',
                                 'source',
                                 os.path.splitext(objectName)[0],
                                 objectName)

        logger.debug("Trying to get \
image data from minio server")
        imageData = None
        imageFormat = ""
        exists = False

        while not exists:
            try:
                logger.debug("Trying to connect..")
                data = minioClient.fget_object(bucketName, objectName, imagePath)

            except:
                time.sleep(0.5)
                continue

            else:
                exists = True
        try:

            logger.debug("Image get successful.")
            # logger.debug("Start writing image file..")

            # with open(imagePath, 'wb+') as file_data:
            #     for d in data.stream(32*1024):
            #         if imageData is None:
            #             imageData = d.split(','.encode('utf-8'))[1]
            #         else:
            #             imageData += d

            #     imageFileData = base64.b64decode(imageData)
            #     file_data.write(imageFileData)
            #     file_data.close()
            #     logger.debug("Successfully wrote image file")

            return imagePath

        except ResponseError as err:
            logger.error(err)

    def imageTilerDeepZoom(self, imagePath, logger):

        creator = deepzoom.ImageCreator(tile_size=128,
                                        tile_overlap=2,
                                        tile_format="png",
                                        image_quality=0.8,
                                        resize_filter="bicubic")
        filename = os.path.split(imagePath)[1]
        filename = os.path.splitext(filename)[0] + '.dzi'
        res_path = os.path.join(os.getcwd(),
                                'imageuploader',
                                'image_tmp',
                                'processed',
                                os.path.splitext(filename)[0],
                                filename
                                )

        logger.debug("Source path: " + imagePath)
        logger.debug("Result path: " + res_path)
        logger.debug("Entering deepzoom api")
        creator.create(imagePath, res_path, logger)

        return res_path

    def imageTilerOpenSlide(self, imagePath, logger):
        SLIDE_CACHE_SIZE = 10
        DEEPZOOM_FORMAT = 'png'
        DEEPZOOM_TILE_SIZE = 254
        DEEPZOOM_OVERLAP = 1
        DEEPZOOM_LIMIT_BOUNDS = True
        DEEPZOOM_TILE_QUALITY = 75

        filename = os.path.split(imagePath)[1]
        filename = os.path.splitext(filename)[0] + '.dzi'
        res_path = os.path.join(os.getcwd(),
                                'imageuploader',
                                'image_tmp',
                                'processed',
                                os.path.splitext(filename)[0],
                                filename
                                )
        tile_dir_path = os.path.join(os.getcwd(),
                                     'imageuploader',
                                     'image_tmp',
                                     'processed',
                                     os.path.splitext(filename)[0],
                                     os.path.splitext(filename)[0] + "_files")

        slide = openslide.OpenSlide(imagePath)
        dzi = deepzoom.DeepZoomGenerator(slide, limit_bounds=True)

        if not os.path.exists(tile_dir_path):
            os.makedirs(tile_dir_path)

        # saving .dzi
        with open(res_path, 'w') as dzi_file:
            dzi_file.write(dzi.get_dzi("png"))
            dzi_file.close()

        # saving tiles
        levels = dzi.level_tiles
        for level in range(len(levels)):
            cols = levels[level][0]
            rows = levels[level][1]
            for col in range(cols):
                for row in range(rows):
                    path = os.path.join(
                        tile_dir_path, str(level),
                        str(col) + "_" + str(row) + ".png")
                    tile = dzi.get_tile(level, (col, row))
                    if not os.path.exists(os.path.split(path)[0]):
                        os.makedirs(os.path.split(path)[0])
                    open(path, 'a').close()
                    tile.save(path)

        return res_path

    def updateImage(self, image, imagePath, logger):

        logger.debug("Start sending to minio server")
        minioClient = Minio(
            '192.168.0.162:9000',
            access_key='FM9GO6CT17O8122165HB',
            secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
            secure=False
        )

        imageName = os.path.splitext(image.image_name)[0] + '.dzi'
        image_oid = image.image_oid
        bucketName = image_oid.bucket_name
        user = image.user
        is_private = image.is_private
        pub_date = image.pub_date
        processed = True
        dataDirPath = os.path.join(
            os.path.split(imagePath)[0],
            os.path.splitext(
                os.path.split(imagePath)[1])[0]+"_files"
        )

        try:
            with open(imagePath, 'rb') as file_data:
                file_stat = os.stat(imagePath)
                minioClient.put_object(
                    bucketName,
                    imageName,
                    file_data,
                    file_stat.st_size,
                    content_type='application/dzi'
                )
                file_data.close()

            logger.debug(
                "Starting upload \
recursively to minio server, starting from " +
                dataDirPath)
            self.uploadRecursively(
                minioClient,
                dataDirPath,
                logger,
                os.path.split(dataDirPath)[0],
                bucketName,
                os.path.split(dataDirPath)[1],
                os.path.splitext(imageName)[0]
                )
            logger.debug("Successfully sent to minio server")

            logger.debug("Copying files to frontend/public/")
            try:
                shutil.copytree(
                    os.path.split(dataDirPath)[0],
                    '/code/frontend_app/deepzoom/' + bucketName)
                logger.debug("[DeepZeeomWrapper] Successfully copied files")

            except Exception as e:
                logger.debug("Error occured copying files: ")
                logger.debug("" + str(e))
                self.__imageQueue.pop()

            logger.debug("Deleting temporary files")
            shutil.rmtree(os.path.split(dataDirPath)[0])
            shutil.rmtree('/code/imageuploader/image_tmp/source/' +
                          os.path.splitext(imageName)[0]
                          )
            logger.debug("Successfully \
deleted temporary files")

            logger.debug("Start update db")

            try:
                if (oid.objects.all().filter(bucket_name=bucketName)
                        .filter(object_name=imageName).exists()):
                        raise Exception

                else:
                        m_oid = oid(
                            url='192.168.0.162:9000',
                            bucket_name=bucketName,
                            object_name=imageName
                        )
                        m_oid.save()
                        m_user = Users.objects.all().filter(name=user).get()
                        m_image = Image(
                            image_name=imageName,
                            image_oid=m_oid,
                            preview_url="",
                            user=m_user,
                            is_private=is_private,
                            pub_date=pub_date,
                            processed=processed
                        )
                        m_image.save()

                        logger.debug("\
Deleting original image from db")
                        m_image2del = Image.objects.all() \
                            .filter(image_oid__bucket_name=bucketName) \
                            .filter(image_name=image.image_name).get()
                        m_image2del.delete()

                        logger.debug("\
Deleting original image from minio")
                        minioClient.remove_object(bucketName, image.image_name)
                        logger.debug("\
Successfully deleted unprocessed image")

            except Exception as e:
                logger.error("[Exception] at DeepZoomWrapper:183 " + e)
                logger.error("Object exists?")
                self.__imageQueue.pop()

            logger.debug("Succesfully updated db")

        except ResponseError as err:
            logger.error("[ResponseError] at DeepZoomWrapper:190 " + err)
            self.__imageQueue.pop()

        return

    def uploadRecursively(self,
                          minioClient,
                          path,
                          logger,
                          baseDir,
                          bucketName,
                          directoryName,
                          imageName
                          ):

        if os.path.isfile(path):
            try:
                filename = os.path.relpath(path, baseDir)
                filename = filename.replace(
                    directoryName, imageName + "_files")

                # logger.debug("Sending filename: " + filename)
                with open(path, 'rb') as file_data:
                    file_stat = os.stat(path)
                    minioClient.put_object(
                        bucketName, filename, file_data, file_stat.st_size)
                    # logger.debug("Sent file: " + filename)
                    file_data.close()

            except Exception as e:
                self.__imageQueue.pop()
                logger.debug(e)

        elif os.path.isdir(path):
            for content in os.listdir(path):
                subPath = os.path.join(path, content)
                # logger.debug("Entering sub directory: " + subPath)
                self.uploadRecursively(minioClient,
                                       subPath,
                                       logger,
                                       baseDir,
                                       bucketName,
                                       directoryName,
                                       imageName
                                       )
#                 logger.debug("\
# Exiting to parent directory" + os.path.split(subPath)[0])

    def handleImage(self, image, logger):

        try:
            start = datetime.datetime.now()
            logger.debug('Started at: ' +
                         time.strftime("%H-%M-%S"))
            bucketName = image.image_oid.bucket_name
            objectName = image.image_name
            logger.debug("bucketName: " +
                         bucketName + ", objectName: " + objectName)

            logger.debug("Entering imageFetcher at: " +
                         time.strftime("%H-%M-%S"))
            imagePath = self.imageFetcher(bucketName, objectName, logger)
            logger.debug("Fetched image path: " + imagePath)

            logger.debug("Entering imageTiler at: " +
                         time.strftime("%H-%M-%S"))

            if (os.path.splitext(imagePath)[1].lower() 
                    in ["jpeg", "jpg", "png"]):
                imagePath_processed = self.imageTilerDeepZoom(imagePath,
                                                              logger)

            elif (os.path.splitext(imagePath)[1].lower()
                    in ["svs", ".tif", "tiff"]):
                imagePath_processed = self.imageTilerOpenSlide(imagePath,
                                                               logger)

            self.updateImage(image, imagePath_processed, logger)
            logger.info("Processing image finished.")
            elapsed = datetime.datetime.now() - start
            ms = elapsed / datetime.timedelta(milliseconds=1)
            logger.info("Processing took " + str(ms) + " ms.")

            self.__imageQueue.pop()
            return

        except Exception as e:
            self.__imageQueue.pop()
            logger.error("Exception occured handling image.")
            logger.error(e)

        return

    def process(self):

        threads = {}

        for image in self.__imageQueue:

            # attatch logging module
            logger = logging.getLogger(name=image.image_name)

            # creating thread
            logger.debug("Creating thread..")
            m_thread = Thread(target=self.handleImage,
                              name=image.image_name,
                              args=(image, logger,))
            m_thread.start()
            threads[m_thread.name] = m_thread

        start = time.time()
        elapsed = time.time() - start
        while threads:
            elapsed = time.time() - start
            if (elapsed % 5 == 0):
                logger.debug("\
processing " + len(threads) + "images for " + elapsed + " seconds.")

            for name, thread in threads:
                if not thread.is_alive():
                    imageName = thread.name
                    threads.pop(imageName, None)