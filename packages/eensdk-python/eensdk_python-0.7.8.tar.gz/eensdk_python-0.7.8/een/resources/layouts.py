def get_layouts(self, include=None, sort=None, pageToken=None, pageSize=None, name=None, name__in=None, name__contains=None, id__in=None, layoutPanes_cameras_bridgeId=None, q=None, qRelevance__gte=None):
    """Auto-generated method for 'getLayouts'

    This endpoint allows you to retrieve all the layouts associated with the account.
It is important to note that after using the pageSize parameter, the "totalSize"  in the response represents the total number of available layouts, not the number of layouts resulting from the query string.


    HTTP Method: GET
    Endpoint: /layouts

    Parameters:
        - include (query): No description provided
        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=3 - Only Three values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400
 * rotationOrder is ordering elements according to the user's list of Layout ids as configured in the user configuration parameter layoutSettings.rotationOrder. Layouts which are not in the list are ordered based on lower priority ordering params if specified, or by the default ordering if not specified.

        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - name (query): Filter to get the layouts with the specified name. The lookup is exact and case insensitive.
        - name__in (query): Filter to get the layouts whose name is on the provided list. The lookup is exact and case insensitive.
        - name__contains (query): Filter to get the layouts whose the name contains the provided substring. The lookup is exact and case insensitive.

        - id__in (query): Filter to get the layouts whose id is on the provided list. The lookup is exact and case insensitive.
        - layoutPanes.cameras.bridgeId (query): Filter to get the layouts that contain cameras of given bridge id.

        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched: `name`, `id`, `accountId`.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).


    Responses:
        - 200: Successfully fetched
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/layouts"
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
    if name is not None:
        params['name'] = name
    if name__in is not None:
        if isinstance(name__in, list):
            params['name__in'] = ','.join(map(str, name__in))
        else:
            params['name__in'] = str(name__in)
    if name__contains is not None:
        params['name__contains'] = name__contains
    if id__in is not None:
        if isinstance(id__in, list):
            params['id__in'] = ','.join(map(str, id__in))
        else:
            params['id__in'] = str(id__in)
    if layoutPanes_cameras_bridgeId is not None:
        params['layoutPanes_cameras_bridgeId'] = layoutPanes_cameras_bridgeId
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


def create_layout(self, body):
    """Auto-generated method for 'createLayout'

    This endpoint allows you to create a layout.

    HTTP Method: POST
    Endpoint: /layouts

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - panes (array): No description provided.
        - settings (object): Object identifying the layout settings
        - name (string): Name of the layout.

    Responses:
        - 201: Layout Created
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 500: No description provided
    """
    endpoint = "/layouts"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def delete_layout(self, layoutId):
    """Auto-generated method for 'deleteLayout'

    This endpoint allows you to delete an existing layout.

    HTTP Method: DELETE
    Endpoint: /layouts/{layoutId}

    Parameters:
        - layoutId (path): No description provided

    Responses:
        - 204: Layout deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: Referenced resource could not be found.
        - 500: No description provided
    """
    endpoint = f"/layouts/{layoutId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_layout(self, layoutId, include=None):
    """Auto-generated method for 'getLayout'

    This endpoint allows you to retrieve info of a specific layout.

    HTTP Method: GET
    Endpoint: /layouts/{layoutId}

    Parameters:
        - layoutId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/layouts/{layoutId}"
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


def update_layout(self, body, layoutId):
    """Auto-generated method for 'updateLayout'

    This endpoint allows you to update a specific layout.

    HTTP Method: PATCH
    Endpoint: /layouts/{layoutId}

    Parameters:
        - layoutId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - panes (array): No description provided.
        - settings (object): Object identifying the layout settings
        - name (string): Name of the layout.

    Responses:
        - 204: Layout Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/layouts/{layoutId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
