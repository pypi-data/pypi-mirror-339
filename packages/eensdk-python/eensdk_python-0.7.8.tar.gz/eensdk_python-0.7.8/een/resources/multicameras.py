def list_multi_cameras(self, locationId__in=None, bridgeId__in=None, q=None, qRelevance__gte=None, sort=None, include=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'listMultiCameras'

    This endpoint allows you to retrieve a list of multi cameras for a given account and location. Multi cameras are devices such as DVRs that have multiple cameras connected.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available multi cameras, not the number of multi cameras resulting from the query string.


    HTTP Method: GET
    Endpoint: /multiCameras

    Parameters:
        - locationId__in (query): List of Location IDs to filter on that is comma separated.
        - bridgeId__in (query): List of Bridge IDs to filter on that is comma separated.
        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched are metadata fields of the camera itself such as `id`, `name`, `notes`, `timezone`, `multiCameraId`, `speakerId` and `tags`; the important ids such as `accountId`, `bridgeId`, and, `locationId`, and metadata of important linked resources such as the location, bridge, share details, device position, device info and the viewports configured for the camera.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).

        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=2 - Only Three values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400 

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
    endpoint = "/multiCameras"
    params = {}
    if locationId__in is not None:
        if isinstance(locationId__in, list):
            params['locationId__in'] = ','.join(map(str, locationId__in))
        else:
            params['locationId__in'] = str(locationId__in)
    if bridgeId__in is not None:
        params['bridgeId__in'] = bridgeId__in
    if q is not None:
        params['q'] = q
    if qRelevance__gte is not None:
        params['qRelevance__gte'] = qRelevance__gte
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
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


def add_multi_camera(self, body):
    """Auto-generated method for 'addMultiCamera'

    This endpoint allows a multi camera to be associated with an account. It can only be called with an end-user account and will fail if called with another type of account.

    HTTP Method: POST
    Endpoint: /multiCameras

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - guid (string): No description provided.
        - name (string): User-defined name for the device.
        - tags (array): No description provided.
        - locationId (string): ID Of the location.
        - bridgeId (string): The bridge a multi camera is connected to. 

        - credentials (object): No description provided.

    Responses:
        - 201: Multi camera added
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request.
        - 500: The request encountered an internal error.
        - 504: The request had a deadline that expired before the operation completed.
    """
    endpoint = "/multiCameras"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_multi_camera(self, multiCameraId, include=None):
    """Auto-generated method for 'getMultiCamera'

    This endpoint allows you to retrieve information about a multi camera based on its ID.

    HTTP Method: GET
    Endpoint: /multiCameras/{multiCameraId}

    Parameters:
        - multiCameraId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/multiCameras/{multiCameraId}"
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


def delete_multi_camera(self, multiCameraId):
    """Auto-generated method for 'deleteMultiCamera'

    This endpoint allows you to dis-associate a multi camera from the account, removing all references, recordings, and events.  
  
This request will be blocked until the multi camera has been fully removed.


    HTTP Method: DELETE
    Endpoint: /multiCameras/{multiCameraId}

    Parameters:
        - multiCameraId (path): No description provided

    Responses:
        - 204: Multi camera deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = f"/multiCameras/{multiCameraId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def update_multi_camera(self, body, multiCameraId):
    """Auto-generated method for 'updateMultiCamera'

    This endpoint allows you to update a multi camera's data based on its ID.

    HTTP Method: PATCH
    Endpoint: /multiCameras/{multiCameraId}

    Parameters:
        - multiCameraId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): User-defined name for the device.
        - notes (string): No description provided.
        - locationId (string): ID Of the location.
        - tags (array): No description provided.

    Responses:
        - 204: Multi camera Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/multiCameras/{multiCameraId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def get_multi_camera_channels(self, multiCameraId):
    """Auto-generated method for 'getMultiCameraChannels'

    This endpoint allows you to retrieve the channel info of a multi camera. This information can be used to add a camera connected to the channel to the account using the /cameras endpoint. The channel details are read-only. To manipulate a new camera use the /cameras endpoint. If the cameraId is not empty then it means that the camera is already added to the account. It is important to note that after using the pageSize parameter, the "totalSize" in  the response represents the total number of available channels, not the number of channels resulting from the query string.


    HTTP Method: GET
    Endpoint: /multiCameras/{multiCameraId}/channels

    Parameters:
        - multiCameraId (path): No description provided
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/multiCameras/{multiCameraId}/channels"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
