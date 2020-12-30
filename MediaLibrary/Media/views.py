from django.shortcuts import render
from .mediaImpl import MediaImpl
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

impl = MediaImpl()


def mediaHome(request: object):
    return render(request, 'index.html', {})

@csrf_exempt
def addItem(request: object) -> object:
    """
    Method adds the new media item to the media catalog.

    :param request: Request Object contains the details of media item to store in catalog.
    :return: Returns the JSON response {'responseCode': ***, 'message': '*****'}
    """

    media_data = json.loads(request.body)
    media_data = {'media_name': media_data.get('mediaName', ''), 'media_type': media_data.get('mediaType', '')}

    # Validation: Check for valid type of media item.
    if media_data['media_type'] not in ['Movies', 'Games', 'Music']:
        return JsonResponse({'message': 'Invalid Media Type', 'responseCode': 400})

    # Validation: Check for duplicate media items in catalog.
    if mediaItemByName(media_data['media_name']):
        return JsonResponse({'message': 'Item {} already exists in db'.format(media_data['media_name']),
                             'responseCode': 400})

    # Call the handler.
    response = impl.addMediaItem(**media_data)

    return JsonResponse(response)


@csrf_exempt
def editItem(request: object) -> object:
    """
    Method used to edit the media item stored in the catalog.

    :param request: Request Object containing request body 'mediaName': media name that needs an update, 'newMediaName':
    New Proposed media name.
    :return: Returns the JSON response {'responseCode': ***, 'message': '*****'}
    """
    media_data = json.loads(request.body)
    media_data = {'media_name': media_data.get('mediaName'), 'new_media_name': media_data.get('newMediaName')}

    response = impl.editMediaItem(**media_data)

    return JsonResponse(response)


@csrf_exempt
def deleteItem(request: object) -> object:
    """
    Method used to delete the media item from the media catalog.

    :param request: Request Object containing request body 'mediaName': Media Item that needs to be removed from catalog
    :return: Returns the JSON response {'responseCode': ***, 'message': '*****'}
    """
    media_data = json.loads(request.body)
    media_data = {'media_name': media_data.get('mediaName')}

    response = impl.deleteMediaItem(**media_data)

    return JsonResponse(response)


def displayItem(request: object, mediatype=None) -> object:
    """
    Method used to display all the media items stored in the catalog. It also categorises the media items
    by mediatype.

    :param request: Request Object
    :param mediatype: Media Type of media item
    :return: Returns the JSON response {'responseCode': ***, 'message': '*****'}
    """

    if mediatype:
        response = categoriseItem(mediatype)
    else:
        response = impl.displayMediaItem()

    return JsonResponse(response, safe=False)


def mediaItemByName(media_name: str) -> object:
    """
    Helper method used to get media item by name.

    :param media_name: media_name of media item.
    :return: Query Object
    """
    try:
        return impl.mediaItemByName(media_name)
    except ObjectDoesNotExist:
        # Log the exception
        pass


def categoriseItem(media_type: str) -> object:
    """
    Helper method used to categorise the media items based on the media_type.

    :param media_type: media_type of media item.
    :return: List of media item details -> [{'timestamp': '***', 'mediaName': '***', 'mediaType': '***'}, ...]
    """

    try:
        result = list()

        query_obj = impl.mediaItemByType(media_type)
        # Iterate through the query object returned from the database.
        for media_item in query_obj:
            result.append({'timeStamp': datetime.strftime(media_item.created_at, "%d/%m/%Y %H:%M:%S"),
                           'mediaName': media_item.media_name,
                           'mediaType': media_item.media_type})
        return result
    except Exception as ex:
        # Log the exception.
        pass
