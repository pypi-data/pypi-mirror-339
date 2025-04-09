def list_switches(self, id__in=None, name__contains=None, id__contains=None, include=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'listSwitches'

    This endpoint allows users to retrieve a paginated list of switches within a given account.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response  represents the total number of available switches, not the number of switches resulting from the query string.


    HTTP Method: GET
    Endpoint: /switches

    Parameters:
        - id__in (query): List of IDs to filter on that is comma separated.
        - name__contains (query): Filter to get the switches whose the name contains the provided substring. The lookup is exact and case insensitive

        - id__contains (query): Filter to get the switches whose the id contains the provided substring. The lookup is exact and case insensitive

        - include (query): No description provided
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/switches"
    params = {}
    if id__in is not None:
        params['id__in'] = id__in
    if name__contains is not None:
        params['name__contains'] = name__contains
    if id__contains is not None:
        params['id__contains'] = id__contains
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


def get_switch(self, switchId, include=None):
    """Auto-generated method for 'getSwitch'

    This endpoint allows users to retrieve a specific switch based on its id.

    HTTP Method: GET
    Endpoint: /switches/{switchId}

    Parameters:
        - switchId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}"
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


def update_switch(self, body, switchId):
    """Auto-generated method for 'updateSwitch'

    This endpoint allows users to update a given switch.

    HTTP Method: PATCH
    Endpoint: /switches/{switchId}

    Parameters:
        - switchId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Switch name

    Responses:
        - 204: Switch Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def update_port(self, body, switchId, portId):
    """Auto-generated method for 'updatePort'

    A specific port can be turned On/Off with this endpoint. A port can also be power cycled.

    HTTP Method: POST
    Endpoint: /switches/{switchId}/ports/{portId}/actions

    Parameters:
        - switchId (path): No description provided
        - portId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - action (string): Possible values:
* `enable` - Turn on the port. * `disable` - Turn off the port. * `reboot` - Power cycle the port.


    Responses:
        - 204: Port Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}/ports/{portId}/actions"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def update_all_ports(self, body, switchId):
    """Auto-generated method for 'updateAllPorts'

    All ports can be turned On, Off or power cycled with this endpoint.

    HTTP Method: POST
    Endpoint: /switches/{switchId}/ports/all/actions

    Parameters:
        - switchId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - action (string): Possible values:
* `enable` - Turn on the port. * `disable` - Turn off the port. * `reboot` - Power cycle the port.


    Responses:
        - 204: Ports Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/switches/{switchId}/ports/all/actions"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
