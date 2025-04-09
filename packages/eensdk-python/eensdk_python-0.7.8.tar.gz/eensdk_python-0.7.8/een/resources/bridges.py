def list_bridges(self, include=None, sort=None, pageToken=None, pageSize=None, locationId__in=None, tags__contains=None, tags__any=None, name__contains=None, name__in=None, name=None, id__in=None, id__contains=None, q=None, qRelevance__gte=None):
    """Auto-generated method for 'listBridges'

    A list of bridges can be retrieved using this endpoint.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number  of available bridges, not the number of bridges resulting from the query string.


    HTTP Method: GET
    Endpoint: /bridges

    Parameters:
        - include (query): No description provided
        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=3 - Only Three values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400

        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - locationId__in (query): List of Location IDs to filter on that is comma separated.
        - tags__contains (query): Only return bridges that have all tags in the list, separated by commas.
        - tags__any (query): Only return bridges that have one or more of the tags in the list, separated by commas.
        - name__contains (query): Filter to get the bridges whose the name contains the provided substring. The lookup is exact and case insensitive

        - name__in (query): Filter to get the bridges whose name is on the provided list. The lookup is exact and case insensitive.
        - name (query): Filter to get the bridges with the specified name. The lookup is exact and case insensitive.
        - id__in (query): Filter to get the bridges whose id is on the provided list. The lookup is exact and case insensitive.
        - id__contains (query): Filter to get the bridges whose the id contains the provided substring. The lookup is exact and case insensitive

        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched: `id`, `accountId`, `name`, `notes`, `tags`, `timeZone.zone`, `devicePosition.floor`, and metadata of important linked resources such as the location.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/bridges"
    params = {}
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if locationId__in is not None:
        if isinstance(locationId__in, list):
            params['locationId__in'] = ','.join(map(str, locationId__in))
        else:
            params['locationId__in'] = str(locationId__in)
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
    if id__contains is not None:
        params['id__contains'] = id__contains
    if q is not None:
        params['q'] = q
    if qRelevance__gte is not None:
        params['qRelevance__gte'] = qRelevance__gte
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_bridge(self, body):
    """Auto-generated method for 'createBridge'

    Create the bridge for the account with given connect id

    HTTP Method: POST
    Endpoint: /bridges

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): User-defined name for the device.
        - connectId (string): The code delivered with a bridge and assigned to it
        - locationId (string): ID Of the location.
        - tags (array): No description provided.

    Responses:
        - 201: Bridge Created
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = "/bridges"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def update_bulk_bridges(self, body=None):
    """Auto-generated method for 'updateBulkBridges'

    This endpoints updates multiple bridges with provided updateField.


    HTTP Method: POST
    Endpoint: /bridges:bulkUpdate

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - ids (array): No description provided.
        - updateFields (object): This defines the parameter that will be updated for list of bridges. Currently, we allow only one parameter to be updated at a time.


    Responses:
        - 201: Bridges updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/bridges:bulkUpdate"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def update_bridge(self, body, bridgeId):
    """Auto-generated method for 'updateBridge'

    Update the bridge for the account with given bridge id

    HTTP Method: PATCH
    Endpoint: /bridges/{bridgeId}

    Parameters:
        - bridgeId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): User-defined name for the device.
        - notes (string): No description provided.
        - locationId (string): ID Of the location.
        - tags (array): No description provided.
        - deviceAddress (object): Address of the device.
        - devicePosition (object): No description provided.

    Responses:
        - 204: Bridge Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/bridges/{bridgeId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def get_bridge(self, bridgeId, include=None):
    """Auto-generated method for 'getBridge'

    Retrieves the given bridge.

    HTTP Method: GET
    Endpoint: /bridges/{bridgeId}

    Parameters:
        - bridgeId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/bridges/{bridgeId}"
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


def delete_bridge(self, bridgeId):
    """Auto-generated method for 'deleteBridge'

    Removes the given bridge from the account, resetting it in the process and removing all cameras that were connected to it.

    HTTP Method: DELETE
    Endpoint: /bridges/{bridgeId}

    Parameters:
        - bridgeId (path): No description provided

    Responses:
        - 204: Bridge deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request.
        - 500: No description provided
    """
    endpoint = f"/bridges/{bridgeId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_bridge_metrics(self, bridgeId, target__in, timestamp__lte=None, timestamp__gte=None, period=None):
    """Auto-generated method for 'getBridgeMetrics'

    Returns metrics data.

    HTTP Method: GET
    Endpoint: /bridges/{bridgeId}/metrics

    Parameters:
        - bridgeId (path): No description provided
        - timestamp__lte (query): Maximum timestamp to list metrics. Defaults to now.
        - timestamp__gte (query): Minimum timestamp to list metrics. Defaults to 7 days ago.
        - target__in (query): Comma separated list of metric types. The following targets are available:
 * `kilobytesOnDisk` - shows how much storage capacity is used on bridge.
 * `availableKilobytesOnDisk` - shows how much storage capacity is not used on bridge.
 * `bytesStored` - shows how much data was stored.
 * `bandwidthBackground` - extra data that contains data from the past
which bridge is sending to try to meet cloud retention goals and the data that are requested from cloud e.g when user is viewing a video.
 * `bandwidthRealtime` - the minimum amount of data, required to keep the bridge operational.
 * `bytesFreed` - shows how much data was freed, includes purges.
 * `bandwidth` - the bandwidth as measured while sending data to the cloud.

        - period (query): Defaults to hour. It performs linear interpolation to get to the target period.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/bridges/{bridgeId}/metrics"
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


def swap_bridge(self, bridgeId, body=None):
    """Auto-generated method for 'swapBridge'

    Swap bridge with a new one.
The original bridge must be offline and disconnected, if not API is going to throw 400 error.
If the GUID is not added to the account or GUID has already been attached to another account API is going to throw 404 error.
If the provided GUID is in wrong format, API is going to throw 400 error.


    HTTP Method: PATCH
    Endpoint: /bridges/{bridgeId}:swap

    Parameters:
        - bridgeId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - guid (string): Represents a new bridge

    Responses:
        - 204: Bridge swap operation success.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/bridges/{bridgeId}:swap"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
