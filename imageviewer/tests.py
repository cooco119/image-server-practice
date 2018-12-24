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

        sample_image_names = [
            "sample_image_1_flower.jpg",
            "sample_image_2_apple.jpg",
            "sample_image_3_bird.jpg",
            "sample_image_4_market.jpg",
            "sample_image_5_stairs.jpg"
        ]
        
        Image.objects.create(
            image_name=sample_image_names[0], 
            image_oid=os.path.join(BASE_DIR, sample_image_names[0]),
            user="Alex",
            is_private=False
        )
        Image.objects.create(
            image_name=sample_image_names[1], 
            image_oid=os.path.join(BASE_DIR, sample_image_names[1]),
            user="Alex",
            is_private=True
        )
        Image.objects.create(
            image_name=sample_image_names[2], 
            image_oid=os.path.join(BASE_DIR, sample_image_names[2]),
            user="Alex",
            is_private=False
        )
        Image.objects.create(
            image_name=sample_image_names[3], 
            image_oid=os.path.join(BASE_DIR, sample_image_names[3]),
            user="jaejun",
            is_private=False
        )
        Image.objects.create(
            image_name=sample_image_names[4], 
            image_oid=os.path.join(BASE_DIR, sample_image_names[4]),
            user="jaejun",
            is_private=True
        )
        

    '''
    Testing GetImageHandler
    '''
    # Test if url configuration is ok
    def test_imageviewer_view_images_url_exists_at_desired_location(self):
        response = self.client.get('/imageviewer/images/')
        self.assertEqual(response.status_code, 200)

    def test_imageviewer_view_accessible_by_name(self):
        response = self.client.get(reverse('images'))
        self.assertEqual(response.status_code, 200)

    # Test if logics are ok
    def test_get_image_handler_if_returns_image_list(self):
        response = self.client.post(reverse('images'), json.dumps({"name":"Alex"}), content_type='application/json')
        responseData = json.loads(response.data)
        image_list = responseData.get("image_list")
        self.assertEqual(type(image_list), type([1,2,3]))

    def test_get_image_handler_if_image_list_contains_image(self):
        response = self.client.post(reverse('images'), json.dumps({"name":"Alex"}), content_type='application/json')
        responseData = json.loads(response.data)
        image_list = responseData.get("image_list")
        self.assertEqual(type(image_list), type([1,2,3]))
        
        # stream_handler = logging.StreamHandler(sys.stdout)
        # logger.addHandler(stream_handler)
        # try: 
        #     logger.info("Images list has " + len(image_list) + " elements.")
        # finally:
        #     logger.removeHandler(stream_handler)
        for i in range(len(image_list)):
            serializer = ImageSerializer(data=image_list[i])
            self.assertEqual(serializer.is_valid(), True, msg="[Image " + str(i) + "] valid image.")

    def test_get_image_handler_if_private_accessible(self):
        response = self.client.post(reverse('images'), json.dumps({"name":"Alex"}), content_type='application/json')
        responseData = json.loads(response.data)
        image_list = responseData.get("image_list")
        
        # test if there's not "Alex"'s image && private
        for i in range(len(image_list)):
            if image_list[i].is_private:
                self.assertEqual(image_list[i].user.name, "Alex")

