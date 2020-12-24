from . import models
from django.db import DatabaseError, DataError, OperationalError
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class GenericImpl:
    def __init__(self):
        pass


class MediaImpl(GenericImpl):
    """
    Implementation of the Media Library.
    """
    def __init__(self):
        GenericImpl.__init__(self)

    def addMediaItem(self, **kwargs: dict):
        """
        Add an item to the media catalog.

        :param kwargs: dictionary {'media_name': '***', 'media_type': '***'}
        :return: dictionary {'responseCode': ***, 'message': '*****'}
        """
        try:
            models.Media(media_name=kwargs.get('media_name'), media_type=kwargs.get('media_type')).save()
            ret_val = {'responseCode': 200, 'message': 'Item inserted successfully'}

        except (DatabaseError, DataError, OperationalError) as ex:
            ret_val = {'responseCode': 500, 'message': 'Error while inserting the element in database'}
        except Exception as ex:
            ret_val = {'responseCode': 500, 'message': 'Unknown Exception'}

        return ret_val

    def editMediaItem(self, **kwargs: dict):
        """
        :param kwargs: dictionary {'media_name': '***', 'new_media_name': '***'}
        :return: dictionary {'responseCode': ***, 'message': '*****'}
        """
        media_name, new_media_name = kwargs.get('media_name'), kwargs.get('new_media_name')

        try:
            # Get media Item by Media Name
            item_obj = self.mediaItemByName(media_name)

            if item_obj:
                # Save the new media name in the database
                item_obj.media_name = new_media_name
                item_obj.save()
            ret_val = {'responseCode': 200, 'message': 'Item updated successfully'}

        except ObjectDoesNotExist as ex:
            ret_val = {'responseCode': 404, 'message': 'Media item does not exist in database'}
        except (DatabaseError, DataError, OperationalError) as ex:
            ret_val = {'responseCode': 500, 'message': 'Error while updating the item in database'}
        except Exception as ex:
            ret_val = {'responseCode': 500, 'message': 'Unknown Exception'}

        return ret_val

    def deleteMediaItem(self, media_name: str):
        """
        Delete an Item from the media catalog.

        :param media_name:
        :return: dictionary {'responseCode': ***, 'message': '*****'}
        """
        try:
            # Get media Item by Media Name
            item_obj = self.mediaItemByName(media_name)
            if item_obj:
                # Delete the media Item
                item_obj.delete()

            ret_val = {'responseCode': 200, 'message': 'Item deleted successfully'}

        except ObjectDoesNotExist as ex:
            ret_val = {'responseCode': 404, 'message': 'Media item {} does not exist in database'.format(media_name)}
        except (DatabaseError, DataError, OperationalError) as ex:
            ret_val = {'responseCode': 500, 'message': 'Error while deleting the item from database'}
        except Exception as ex:
            ret_val = {'responseCode': 500, 'message': 'Unknown Exception.'}

        return ret_val

    def displayMediaItem(self):
        """
        Display all items in the media catalog.

        :return: List of media items [{'timestamp': '***', 'mediaName': '***', 'mediaType': '***'}, ...]
        """
        try:
            # Get all media items
            query_obj = models.Media.objects.all()
            result, ret_val = list(), dict()

            # Iterate through the list of media items.
            for media_item in query_obj:
                result.append({'timeStamp': datetime.strftime(media_item.created_at, "%d/%m/%Y %H:%M:%S"),
                               'mediaName': media_item.media_name,
                               'mediaType': media_item.media_type})

            return result

        except (DatabaseError, DataError, OperationalError) as ex:
            ret_val = {'responseCode': 500, 'message': 'Error while fetching items from database'}
        except Exception as ex:
            ret_val = {'responseCode': 500, 'message': 'Unknown Exception.'}

        return ret_val

    def mediaItemByName(self, media_name: str):
        """
        Helper method to get media item by name.

        :param media_name: Media Name of the media_item.
        :return: Query Object
        """
        try:
            return models.Media.objects.get(media_name=media_name)
        except (DatabaseError, DataError, OperationalError) as ex:
            raise
        except Exception as ex:
            raise

    def mediaItemByType(self, media_type: str):
        """
        Helper method to get all media items by media type.

        :param media_type: Media Type of the Media Item.
        :return: Query Object
        """
        try:
            return models.Media.objects.filter(media_type=media_type)
        except (DatabaseError, DataError, OperationalError) as ex:
            raise
        except Exception as ex:
            raise
