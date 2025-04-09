def get_id_p_groups(self, pageToken=None, pageSize=None, name__contains=None, include=None):
    """Auto-generated method for 'getIdPGroups'

    This endpoint returns a list of all IDP groups in current user's account.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents  the total number of available IDP group, not the number of IDP group resulting from the query string.


    HTTP Method: GET
    Endpoint: /idPGroups

    Parameters:
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - name__contains (query): Filter to get the groups whose names contain the provided substring. The lookup is exact but case-insensitive.

        - include (query): No description provided

    Responses:
        - 200: List of IDP groups.
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/idPGroups"
    params = {}
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if name__contains is not None:
        params['name__contains'] = name__contains
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


def get_id_p_group_assignments(self, groupId__in=None, targetType__in=None, targetId__in=None):
    """Auto-generated method for 'getIdPGroupAssignments'

    This endpoint allows you to retrieve a list of IDP group assignments with pagination and filter parameters.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents  the total number of available IDP group assignments, not the number of IDP group assignments resulting from  the query string.


    HTTP Method: GET
    Endpoint: /idPGroupAssignments

    Parameters:
        - unknown (None): No description provided
        - groupId__in (query): Filter to get IDP group assignments whose groupId is on the provided list.  The lookup is exact but case-insensitive.

        - targetType__in (query): Filter to get IDP group assignments whose targetType is on the provided list.  The lookup is exact but case-insensitive.

        - targetId__in (query): Filter to get IdP group assignments whose targetId is on the provided list.  The lookup is exact but case-insensitive.


    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/idPGroupAssignments"
    params = {}
    if groupId__in is not None:
        if isinstance(groupId__in, list):
            params['groupId__in'] = ','.join(map(str, groupId__in))
        else:
            params['groupId__in'] = str(groupId__in)
    if targetType__in is not None:
        if isinstance(targetType__in, list):
            params['targetType__in'] = ','.join(map(str, targetType__in))
        else:
            params['targetType__in'] = str(targetType__in)
    if targetId__in is not None:
        if isinstance(targetId__in, list):
            params['targetId__in'] = ','.join(map(str, targetId__in))
        else:
            params['targetId__in'] = str(targetId__in)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_id_p_group_assignments(self, body=None):
    """Auto-generated method for 'createIdPGroupAssignments'

    This endpoint allows you to create multiple IDP group assignments in one request.

    HTTP Method: POST
    Endpoint: /idPGroupAssignments:bulkCreate

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Responses:
        - 200: Operations performed successfully
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/idPGroupAssignments:bulkCreate"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def delete_id_p_group_assignments(self, body=None):
    """Auto-generated method for 'deleteIdPGroupAssignments'

    This endpoint allows you to delete multiple IDP group assignments in one request.

    HTTP Method: POST
    Endpoint: /idPGroupAssignments:bulkDelete

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - ids (array): No description provided.

    Responses:
        - 200: Operations performed successfully
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/idPGroupAssignments:bulkDelete"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
