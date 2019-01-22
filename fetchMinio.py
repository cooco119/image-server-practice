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

    numThreads = 0
    MAX_THREAD_NUMBER = 4
    threadList = []
    threadIdxToBePoped = []
    while True:
        if numThreads < MAX_THREAD_NUMBER and not queue.empty():
            for i in range(MAX_THREAD_NUMBER - numThreads - 1):
                m_bucket = queue.get()
                m_thread = Thread(target=fetch,
                                  name=m_bucket.name,
                                  args=(m_bucket, ))
                m_thread.start()
                threadList.append(m_thread)
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
        try:
            for idx in threadIdxToBePoped:
                threadList.pop(idx)
            threadIdxToBePoped = []
        except Exception as e:
            logger.Error(e)

        if len(threadList) == 0:
            return


def startInNewProcess():
    print("Forking into new process")
    print('PID: ', os.getpid())
    setQueueAndStart()

if __name__ == "__main__":
    setQueueAndStart()