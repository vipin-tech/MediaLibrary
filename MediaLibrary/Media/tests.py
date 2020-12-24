from django.test import TestCase
from datetime import datetime
from .models import Media
import uuid
from django.urls import reverse
import json
from django.core.exceptions import ObjectDoesNotExist


# Test Cases for Models File.
class ModelTestCase(TestCase):

    def setUp(self) -> None:
        self.item = Media()
        self.item.created_at = datetime.now()
        self.item.updated_at = datetime.now()
        self.item.media_id = uuid.uuid4()
        self.item.media_name = 'Roar'
        self.item.media_type = 'Music'
        self.item.save()

    def test_fields(self):
        media_item = Media.objects.get(media_name='Roar')
        self.assertEqual(media_item.media_name, self.item.media_name)
        self.assertEqual(media_item.media_type, self.item.media_type)


# Test Cases for Views File.
class ViewTestCase(TestCase):
    def setUp(self) -> None:
        self.item = Media()
        self.item.created_at = datetime.now()
        self.item.updated_at = datetime.now()
        self.item.media_id = uuid.uuid4()
        self.item.media_name = 'Avengers'
        self.item.media_type = 'Movies'
        self.item.save()

    def test_addItem(self):
        # Proper data
        req_data = {'mediaName': 'Roar', 'mediaType': 'Music'}

        response = self.client.post(reverse('AddMedia'), data=json.dumps(req_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_editItem(self):
        req_data = {'mediaName': 'Roar', 'newMediaName': 'Lean On'}
        response = self.client.put(reverse('EditMedia'), data=json.dumps(req_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_deleteItem(self):
        req_data = {'mediaName': 'Roar'}
        response = self.client.delete(reverse('DeleteMedia'), data=json.dumps(req_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_displayItem(self):
        response = self.client.get(reverse('DisplayMedia'))
        self.assertEqual(response.status_code, 200)

    def test_mediaItemByName(self):
        media_item = Media.objects.get(media_name='Avengers')
        self.assertEqual(media_item.media_name, 'Avengers')

    def test_categoriseItem(self):
        media_item = Media.objects.get(media_name='Avengers')
        self.assertEqual(media_item.media_type, 'Movies')


# Test Cases for MediaImpl File.
class MediaImplTestCase(TestCase):
    def setUp(self) -> None:
        self.item = Media()
        self.item.created_at = datetime.now()
        self.item.updated_at = datetime.now()
        self.item.media_id = uuid.uuid4()
        self.item.media_name = 'Avengers'
        self.item.media_type = 'Movies'
        self.item.save()

    def test_addMediaItem(self):
        media_item = Media()
        media_item.media_name = 'Roar'
        media_item.media_type = 'Music'
        media_item.save()

        # Get the query obj.
        query_obj = Media.objects.get(media_name='Roar')

        self.assertEqual(media_item.media_name, query_obj.media_name)

    def test_editMediaItem(self):
        query_obj = Media.objects.get(media_name='Avengers')
        query_obj.media_name = 'Spiderman'
        query_obj.save()

        # Get the query obj.
        query_obj = Media.objects.get(media_name='Spiderman')

        self.assertEqual(query_obj.media_name, 'Spiderman')

    def test_deleteMediaItem(self):
        query_obj = Media.objects.get(media_name='Avengers')

        if query_obj:
            query_obj.delete()

        self.assertRaises(ObjectDoesNotExist, lambda: Media.objects.get(media_name='Avengers'))

    def test_displayMediaItem(self):
        query_obj = Media.objects.all()
        self.assertIsNotNone(query_obj)
        self.assertEqual(query_obj[0].media_name, 'Avengers')

    def test_mediaItemByName(self):
        media_item = Media.objects.get(media_name='Avengers')
        self.assertEqual(media_item.media_name, 'Avengers')

    def test_mediaItemByType(self):
        media_item = Media.objects.get(media_name='Avengers')
        self.assertEqual(media_item.media_type, 'Movies')