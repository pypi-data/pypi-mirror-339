def list_media(self, deviceId, type, mediaType, startTimestamp__gte, endTimestamp__lte=None, coalesce=None, include=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'listMedia'

    This endpoint requests a list of intervals for which there are recordings for the given type and
mediaType. If no endTimestamp__lte (formatted according to ISO 8601) is given, then the
results until now are returned.

Note: The ISO 8601 timestamp format is a standardized format for representing date
and time information. It uses the format 'YYYY-MM-DDTHH:MM:SS.sss±hh:mm' where
"T" is the separator between the date and time portions.


    HTTP Method: GET
    Endpoint: /media

    Parameters:
        - deviceId (query): The ID of the device that generates the media.
        - type (query): The stream type of the device used to generate the media.
        - mediaType (query): The type of media that is queried.
        - startTimestamp__gte (query): Minimum timestamp from which you want to list recordings. Timestamps are according to ISO 8601.
        - endTimestamp__lte (query): Maximum timestamp till which you want to list recordings.
        - coalesce (query): If true, we coalesce connected intervals into a single. An interval is seen as connected if the end time and start time are exactly the same.
        - include (query): No description provided
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/media"
    params = {}
    if deviceId is not None:
        params['deviceId'] = deviceId
    if type is not None:
        params['type'] = type
    if mediaType is not None:
        params['mediaType'] = mediaType
    if startTimestamp__gte is not None:
        params['startTimestamp__gte'] = startTimestamp__gte
    if endTimestamp__lte is not None:
        params['endTimestamp__lte'] = endTimestamp__lte
    if coalesce is not None:
        params['coalesce'] = coalesce
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_recorded_image(self, deviceId=None, pageToken=None, type=None, timestamp__lt=None, timestamp__lte=None, timestamp=None, timestamp__gte=None, timestamp__gt=None, overlayId__in=None, include=None):
    """Auto-generated method for 'getRecordedImage'

    This endpoint requests an image around a timestamp formatted according to ISO 8601. It can be specified if the timestamp must match exactly, or if it can be
before or after. Alternatively, by giving pageToken, the next/previous image from the last image is returned. In this case, none of the other parameters
are used.

Be aware that the image type `main` is rate-limited, and should not be used in quick succession. Additionally, it requires that a recording is available
at the given timestamp param. If no recording is available at the given timestamp param a 404 NOT FOUND will be returned.

In a single request, one of the timestamp parameter needs to be specified.

If an overlay is requested in the `include` parameter, then at least one overlayId must be provided as part of the `overlayId__in` parameter.
The list of available overlay ids can be retrieved using the GET /media/recordedImage.jpeg:listFieldValues API.


    HTTP Method: GET
    Endpoint: /media/recordedImage.jpeg

    Parameters:
        - deviceId (query): The ID of the device that generates the media.
        - pageToken (query): Token provided by `X-Een-NextToken` or `X-Een-PrevToken` header of a previous image call. If
this parameter is present no other parameters are required, and any sent will be ignored

        - type (query): The stream type of the device used to generate the media.
        - timestamp__lt (query): Return first image with timestamp less then.
        - timestamp__lte (query): Return first image with timestamp less or equal.
        - timestamp (query): Return image at this exact timestamp.
        - timestamp__gte (query): Return first image with timestamp greater or equal.
        - timestamp__gt (query): Return first image with timestamp greater then.
        - overlayId__in (query): What info will be included in the returned overlay. At least one id must be provided if an overlay is requested for the `include` parameter.
        - include (query): Extra options that can be included in the api response:
 - overlayEmbedded: draws the overlay on top of the source image resulting in a single jpeg
 - overlaySvgHeader: adds the `X-Een-OverlaySvg` header containing the overlays as a SVG image


    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/media/recordedImage.jpeg"
    params = {}
    if deviceId is not None:
        params['deviceId'] = deviceId
    if pageToken is not None:
        params['pageToken'] = pageToken
    if type is not None:
        params['type'] = type
    if timestamp__lt is not None:
        params['timestamp__lt'] = timestamp__lt
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if timestamp is not None:
        params['timestamp'] = timestamp
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__gt is not None:
        params['timestamp__gt'] = timestamp__gt
    if overlayId__in is not None:
        if isinstance(overlayId__in, list):
            params['overlayId__in'] = ','.join(map(str, overlayId__in))
        else:
            params['overlayId__in'] = str(overlayId__in)
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_live_image(self, deviceId, type):
    """Auto-generated method for 'getLiveImage'

    This endpoint allows users to get a new image from the device. This call will wait until the image is available.


    HTTP Method: GET
    Endpoint: /media/liveImage.jpeg

    Parameters:
        - deviceId (query): The ID of the device that generates the media.
        - type (query): The stream type of the device used to generate the media.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
        - 503: The service or resource is currently not available
    """
    endpoint = "/media/liveImage.jpeg"
    params = {}
    if deviceId is not None:
        params['deviceId'] = deviceId
    if type is not None:
        params['type'] = type
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
