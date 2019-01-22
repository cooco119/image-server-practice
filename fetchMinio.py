from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from pathlib import PurePath, Path
import os
from threading import Thread
from queue import Queue
import logging

logger = logging.getLogger(name=__name__)

minioClient = Minio(
    '192.168.0.162:9000',
    access_key='FM9GO6CT17O8122165HB',
    secret_key='yLyai1DFC03hzN17srK0PvYTIZFvHDnDxRKYAjK4',
    secure=False
    )
queue = Queue()


def fetch(bucket):
    pwd = './frontend_app/deepzoom/'
    objects = minioClient \
        .list_objects_v2(bucket.name, recursive=True)
    for obj in objects:
        resPath = os.path.join(
            pwd, obj.bucket_name, obj.object_name)
        if os.path.exists(resPath):
            continue
        if not obj.is_dir:
            minioClient.fget_object(
                obj.bucket_name, obj.object_name, resPath)
        else:
            os.mkdir(resPath)
    return


def setQueueAndStart():
    buckets = minioClient.list_buckets()
    for bucket in buckets:
        queue.put(bucket)
    print("Start pulling from minio")

    numThreads = 0
    MAX_THREAD_NUMBER = 4
    threadList = []
    threadIdxToBePoped = []
    threadStr = ""
    for i in range(len(threadList)):
        threadStr += threadList[i].name + " "
    print('Thread List: ' + threadStr)
    while True:
        if numThreads <= MAX_THREAD_NUMBER and not queue.empty():
            for i in range(MAX_THREAD_NUMBER - numThreads - 1):
                m_bucket = queue.get()
                m_thread = Thread(target=fetch,
                                  name=m_bucket.name,
                                  args=(m_bucket, ))
                m_thread.start()
                threadList.append(m_thread)
                writeStatus(threadList)
                print("Start pulling " + m_bucket.name)
                numThreads += 1
            
        for i in range(len(threadList)):
            thread = threadList[i]
            try:
                thread.join(timeout=0.05)
            except:
                print("Thread " + thread.name + " is still running")
            if not thread.is_alive():
                threadIdxToBePoped.append(i)
                finishedBucketName = thread.name
                print("Successfully pulled " + finishedBucketName)
                numThreads -= 1

        if threadIdxToBePoped:
            threadIdxToBePoped.sort(reverse=True)
            for idx in threadIdxToBePoped:
                try:
                    threadList.pop(idx)
                except Exception as e:
                    logger.error(e)
                    threadIdxToBePoped.remove(idx)
            threadIdxToBePoped = []

        if len(threadList) == 0:
            return


def writeStatus(threadList):
    print('\r')
    threadStr = ""
    for i in range(len(threadList)):
        threadStr += threadList[i].name + " "
    print('Thread List: ' + threadStr)
if __name__ == "__main__":
    setQueueAndStart()