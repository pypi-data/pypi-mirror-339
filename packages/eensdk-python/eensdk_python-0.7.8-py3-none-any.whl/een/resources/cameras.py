def list_cameras(self, locationId__in=None, bridgeId__in=None, multiCameraId=None, multiCameraId__ne=None, multiCameraId__in=None, tags__contains=None, tags__any=None, packages__contains=None, layoutId=None, name__contains=None, name__in=None, name=None, id__in=None, id__notIn=None, id__contains=None, shareDetails_shared=None, shareDetails_accountId=None, shareDetails_firstResponder=None, deviceInfo_directToCloud=None, speakerId__in=None, q=None, qRelevance__gte=None, enabledAnalytics__contains=None, include=None, pageToken=None, pageSize=None, sort=None):
    """Auto-generated method for 'listCameras'

    This endpoint allows you to retrieve a list of cameras associated with the account, with the ability to filter by account ID, location ID, bridge ID, multi-camera ID, and tags. It also supports pagination and the ability to include additional information about cameras.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available cameras, not the number of cameras resulting from the query string.


    HTTP Method: GET
    Endpoint: /cameras

    Parameters:
        - locationId__in (query): List of Location IDs to filter on that is comma separated.
        - bridgeId__in (query): List of Bridge IDs to filter on that is comma separated.
        - multiCameraId (query): Filter to get cameras with given multiCameraId. multiCameraId=null returns cameras that are not multi camera cameras.
        - multiCameraId__ne (query): Filter to get cameras with multiCameraId that is not equal to given value.
        - multiCameraId__in (query): List of multi camera IDs to filter on that is comma seperated.
        - tags__contains (query): Only return cameras that have all tags in the list, separated by commas.
        - tags__any (query): Only return cameras that have one or more of the tags in the list, separated by commas.
        - packages__contains (query): Only return cameras that have enabled all packages in the list, separated by commas.
        - layoutId (query): Filter to get cameras that are part of the given layout.
        - name__contains (query): Filter to get the cameras whose the name contains the provided substring. The lookup is exact and case insensitive

        - name__in (query): Filter to get the cameras whose name is on the provided list. The lookup is exact and case insensitive.
        - name (query): Filter to get the cameras with the specified name. The lookup is exact and case insensitive.
        - id__in (query): Filter to get the cameras whose id is on the provided list. The lookup is exact and case insensitive.
        - id__notIn (query): Filter to exlude the cameras whose ids are in the provided list. The lookup is exact and case insensitive.
        - id__contains (query): Filter to get the cameras whose the id contains the provided substring. The lookup is exact and case insensitive

        - shareDetails.shared (query): If set to `true`, only cameras that are shared with the current account by another account will be returned. If set to `false`, the cameras that are shared with the current account will be filtered out.

        - shareDetails.accountId (query): Filter to get the cameras that are shared from the provided account.
        - shareDetails.firstResponder (query): If set to `true`, only cameras that are shared with the current account using the "First responder" feature will be returned. If set to `false`, the cameras that are shared with the current account using the "First responder" feature will be filtered out.

        - deviceInfo.directToCloud (query): If set to `true`, only cameras that connect directly to the VMS cloud, and not through a bridge will be returned. If set to `false`, the cameras that connect directly to the VMS cloud will be filtered out.

        - speakerId__in (query): Filter to get cameras that are a part of the given speaker esn.
        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched are metadata fields of the camera itself such as `id`, `name`, `notes`, `timezone`, `multiCameraId`, `speakerId` and `tags`; the important ids such as `accountId`, `bridgeId`, and, `locationId`, and metadata of important linked resources such as the location, bridge, share details, device position, device info and the viewports configured for the camera.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).

        - enabledAnalytics__contains (query): Only return cameras that have enabled all analytics in the comma-separated list.
        - include (query): No description provided
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=3 - Only Three values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400 


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/cameras"
    params = {}
    if locationId__in is not None:
        if isinstance(locationId__in, list):
            params['locationId__in'] = ','.join(map(str, locationId__in))
        else:
            params['locationId__in'] = str(locationId__in)
    if bridgeId__in is not None:
        params['bridgeId__in'] = bridgeId__in
    if multiCameraId is not None:
        params['multiCameraId'] = multiCameraId
    if multiCameraId__ne is not None:
        params['multiCameraId__ne'] = multiCameraId__ne
    if multiCameraId__in is not None:
        params['multiCameraId__in'] = multiCameraId__in
    if tags__contains is not None:
        if isinstance(tags__contains, list):
            params['tags__contains'] = ','.join(map(str, tags__contains))
        else:
            params['tags__contains'] = str(tags__contains)
    if tags__any is not None:
        if isinstance(tags__any, list):
            params['tags__any'] = ','.join(map(str, tags__any))
        else:
            params['tags__any'] = str(tags__any)
    if packages__contains is not None:
        if isinstance(packages__contains, list):
            params['packages__contains'] = ','.join(map(str, packages__contains))
        else:
            params['packages__contains'] = str(packages__contains)
    if layoutId is not None:
        params['layoutId'] = layoutId
    if name__contains is not None:
        params['name__contains'] = name__contains
    if name__in is not None:
        if isinstance(name__in, list):
            params['name__in'] = ','.join(map(str, name__in))
        else:
            params['name__in'] = str(name__in)
    if name is not None:
        params['name'] = name
    if id__in is not None:
        if isinstance(id__in, list):
            params['id__in'] = ','.join(map(str, id__in))
        else:
            params['id__in'] = str(id__in)
    if id__notIn is not None:
        if isinstance(id__notIn, list):
            params['id__notIn'] = ','.join(map(str, id__notIn))
        else:
            params['id__notIn'] = str(id__notIn)
    if id__contains is not None:
        params['id__contains'] = id__contains
    if shareDetails_shared is not None:
        params['shareDetails_shared'] = shareDetails_shared
    if shareDetails_accountId is not None:
        params['shareDetails_accountId'] = shareDetails_accountId
    if shareDetails_firstResponder is not None:
        params['shareDetails_firstResponder'] = shareDetails_firstResponder
    if deviceInfo_directToCloud is not None:
        params['deviceInfo_directToCloud'] = deviceInfo_directToCloud
    if speakerId__in is not None:
        if isinstance(speakerId__in, list):
            params['speakerId__in'] = ','.join(map(str, speakerId__in))
        else:
            params['speakerId__in'] = str(speakerId__in)
    if q is not None:
        params['q'] = q
    if qRelevance__gte is not None:
        params['qRelevance__gte'] = qRelevance__gte
    if enabledAnalytics__contains is not None:
        if isinstance(enabledAnalytics__contains, list):
            params['enabledAnalytics__contains'] = ','.join(map(str, enabledAnalytics__contains))
        else:
            params['enabledAnalytics__contains'] = str(enabledAnalytics__contains)
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def add_camera(self, body):
    """Auto-generated method for 'addCamera'

    Associates a camera with the account. This can only be called with an end-user account, and will result in an error if tried with any other type of account.


    HTTP Method: POST
    Endpoint: /cameras

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - registrationStrategy (string): Cameras can be added in multiple ways, and this field indicates how this specific camera should be added. Possible methods:
 * `bridge`: Associate a camera found with `GET /api/v3.0/availableDevices` with one of the bridges that found it.
 * `rtspUrl`: Define a camera by giving a RTSP URL to retrieve its live stream and the bridge that should connect to it.
 * `cameraDirect`: Register a camera by its MAC address regardless of its physical location and without needing a bridge.
 * `channel`: Associate a channel camera with its parent multi camera.


    Responses:
        - 201: Camera added
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request.
        - 500: The request encountered an internal error.
        - 504: The request had a deadline that expired before the operation completed.
    """
    endpoint = "/cameras"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def update_bulk_cameras(self, body=None):
    """Auto-generated method for 'updateBulkCameras'

    This endpoint allows the developer to update multiple cameras at once by providing update fields.


    HTTP Method: POST
    Endpoint: /cameras:bulkUpdate

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - ids (array): No description provided.
        - updateFields (object): This defines the parameter that will be updated for list of cameras. Currently, we allow only one parameter to be updated at a time.


    Responses:
        - 201: Cameras updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/cameras:bulkUpdate"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_camera(self, cameraId, include=None):
    """Auto-generated method for 'getCamera'

    Retrieves the given camera.

    HTTP Method: GET
    Endpoint: /cameras/{cameraId}

    Parameters:
        - cameraId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}"
    params = {}
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


def delete_camera(self, cameraId):
    """Auto-generated method for 'deleteCamera'

    This endpoint disassociates the camera from the account, removing all references, recordings, and events, and in some cases resetting the camera to factory default settings. This request will be blocked until the camera has been fully removed.


    HTTP Method: DELETE
    Endpoint: /cameras/{cameraId}

    Parameters:
        - cameraId (path): No description provided

    Responses:
        - 204: Camera deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def update_camera(self, body, cameraId):
    """Auto-generated method for 'updateCamera'

    This endpoint allows the developers to update a specific camera by providing update fields.

    HTTP Method: PATCH
    Endpoint: /cameras/{cameraId}

    Parameters:
        - cameraId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): User-defined name for the device.
        - notes (string): No description provided.
        - speakerId (string): Id of the speaker.
        - locationId (string): ID Of the location.
        - tags (array): No description provided.
        - devicePosition (object): No description provided.
        - deviceAddress (object): Address of the device.
        - publicSafetySharing (object): No description provided.

    Responses:
        - 204: Camera Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def put_camera_tunnel(self, body, cameraId):
    """Auto-generated method for 'putCameraTunnel'

    Opens a camera tunnel. As this API is intended for incidental access to the cameras UI, it should not be used for general API integration.


    HTTP Method: PUT
    Endpoint: /cameras/{cameraId}/tunnel

    Parameters:
        - cameraId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}/tunnel"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PUT',
        params=params,
        data=data,
    )


def delete_camera_tunnel(self, cameraId):
    """Auto-generated method for 'deleteCameraTunnel'

    Deletes a camera tunnel.


    HTTP Method: DELETE
    Endpoint: /cameras/{cameraId}/tunnel

    Parameters:
        - cameraId (path): No description provided

    Responses:
        - 204: Camera tunnel deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}/tunnel"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_camera_metrics(self, cameraId, target__in, timestamp__lte=None, timestamp__gte=None, period=None):
    """Auto-generated method for 'getCameraMetrics'

    Returns metrics data.

    HTTP Method: GET
    Endpoint: /cameras/{cameraId}/metrics

    Parameters:
        - cameraId (path): No description provided
        - timestamp__lte (query): Maximum timestamp to list metrics. Defaults to now.
        - timestamp__gte (query): Minimum timestamp to list metrics. Defaults to 7 days ago.
        - target__in (query): Comma separated list of metric types. The following targets are available:
 * `kilobytesOnDisk` - shows how much storage capacity is used on bridge.
 * `bytesPurged` - shows how much data was purged. Data is marked as purged if it is removed before Minimum On Premise Retention is met.
 * `bytesStored` - shows how much data was stored.
 * `bytesFreed` - shows how much data was freed, includes purges.
 * `bandwidthBackground` - extra data that contains data from the past
which bridge is sending to try to meet cloud retention goals and the data that are requested from cloud e.g when user is viewing a video.
 * `bandwidthRealtime` - the minimum amount of data, required to keep the camera operational.

        - period (query): Defaults to hour. It performs linear interpolation to get to the target period.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}/metrics"
    params = {}
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if target__in is not None:
        if isinstance(target__in, list):
            params['target__in'] = ','.join(map(str, target__in))
        else:
            params['target__in'] = str(target__in)
    if period is not None:
        params['period'] = period
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def swap_camera(self, cameraId, body=None):
    """Auto-generated method for 'swapCamera'

    Swap any camera with a new one.
If the device is not visible by the bridge, API is going to throw a 404 error.
If the GUID has already been attached to the account, API is going to throw a 409 error.
If the provided GUID is in wrong format, API is going to throw 400 error.


    HTTP Method: PATCH
    Endpoint: /cameras/{cameraId}:swap

    Parameters:
        - cameraId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - guid (string): Represents a new camera

    Responses:
        - 204: Camera swap operation success.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}:swap"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
