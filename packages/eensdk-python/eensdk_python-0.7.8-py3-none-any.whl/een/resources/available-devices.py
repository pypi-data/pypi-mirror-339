def list_available_devices(self, deviceType__in, state__in=None, bridgeId__in=None, pageToken=None, pageSize=None, include=None):
    """Auto-generated method for 'listAvailableDevices'

    This endpoint returns a list of all devices found by the bridges in the account that have not yet been added. Devices of a certain type will not be reported in the response if the user does not have permission to add them. Since adding specific device types requires calling a device-type-specific API, it is recommended to filter on the devices supported by the cameras, rather than retrieving "all" types.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available devices, not the number of devices resulting from the query string.


    HTTP Method: GET
    Endpoint: /availableDevices

    Parameters:
        - deviceType__in (query): List of device types that are supported by the client. Required as new device types might be added at any time, which might need client (parser) changes before they are supported.

        - state__in (query): List of different device states. If provided, the response will only contain devices with provided states.

        - bridgeId__in (query): Filter to get the available devices whose bridge id is on the provided list. The lookup is exact and case insensitive
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/availableDevices"
    params = {}
    if deviceType__in is not None:
        if isinstance(deviceType__in, list):
            params['deviceType__in'] = ','.join(map(str, deviceType__in))
        else:
            params['deviceType__in'] = str(deviceType__in)
    if state__in is not None:
        if isinstance(state__in, list):
            params['state__in'] = ','.join(map(str, state__in))
        else:
            params['state__in'] = str(state__in)
    if bridgeId__in is not None:
        params['bridgeId__in'] = bridgeId__in
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
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
