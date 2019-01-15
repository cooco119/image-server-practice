from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from models.models import Users
from models.models import Image
import json
from PIL import Image as ImageHandler
from models.serializers import ImageSerializer
import os
import logging
import sys


# Create your tests here.
class ImageviewerTestCase(TestCase):
    logger = logging.getLogger()
    logger.level = logging.DEBUG

    def setup(self):
        Users.objects.create(name="Alex")
        Users.objects.create(name="jaejun")
        Users.objects.create(name="Bob")
        Users.objects.create(name="Tom")

        sample_image_names = [
            "sample_image_1_flower.jpg",
            "sample_image_2_apple.jpg",
            "sample_image_3_bird.jpg",
            "sample_image_4_market.jpg",
            "sample_image_5_stairs.jpg"
        ]

        # Image.objects.create(
        #     image_name=sample_image_names[0],
        #     image_oid=os.path.join(BASE_DIR, sample_image_names[0]),
        #     user="Alex",
        #     is_private=False
        # )
        # Image.objects.create(
        #     image_name=sample_image_names[1],
        #     image_oid=os.path.join(BASE_DIR, sample_image_names[1]),
        #     user="Alex",
        #     is_private=True
        # )
        # Image.objects.create(
        #     image_name=sample_image_names[2],
        #     image_oid=os.path.join(BASE_DIR, sample_image_names[2]),
        #     user="Alex",
        #     is_private=False
        # )
        # Image.objects.create(
        #     image_name=sample_image_names[3],
        #     image_oid=os.path.join(BASE_DIR, sample_image_names[3]),
        #     user="jaejun",
        #     is_private=False
        # )
        # Image.objects.create(
        #     image_name=sample_image_names[4],
        #     image_oid=os.path.join(BASE_DIR, sample_image_names[4]),
        #     user="jaejun",
        #     is_private=True
        # )

    # def test_imageviewer_view_get_workspaces_via_absolute_url(self):
    #     response = self.client.get('/imageviewer/Alex/workspaces/')
    #     self.assertEqual(response.status_code, 200)

    # def test_imageviewer_view_accessible_by_name(self):
    #     response = self.client.get(reverse('images'))
    #     self.assertEqual(response.status_code, 200)