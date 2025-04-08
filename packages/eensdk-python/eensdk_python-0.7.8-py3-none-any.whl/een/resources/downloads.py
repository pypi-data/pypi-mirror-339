def get_downloads(self, sort=None, mimeType=None, mimeType__contains=None, createTimestamp__lte=None, createTimestamp__gte=None, expireTimestamp__lte=None, expireTimestamp__gte=None, directory=None, directory__contains=None, name=None, name__contains=None, notes__contains=None, size__lte=None, size__gte=None, tags=None, tags__any=None, tags__contains=None, include=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'getDownloads'

    Returns a list of downloaded items.

    HTTP Method: GET
    Endpoint: /downloads

    Parameters:
        - sort (query): List of fields that should be sorted. Use "-" and the field name to specify descending results. Use "+" and the field name to specify ascending results. By default, results are sorted by create timestamp in descending order.
        - mimeType (query): Exact content type.
        - mimeType__contains (query): Content type contains filter.
        - createTimestamp__lte (query): Maximum timestamp for file creation date.
        - createTimestamp__gte (query): Minimum timestamp for file creation date.
        - expireTimestamp__lte (query): Maximum timestamp for file expiration date.
        - expireTimestamp__gte (query): Minimum timestamp for file expiration date.
        - directory (query): Name of parent directory.
        - directory__contains (query): Item directory contains filter.
        - name (query): Exact name of the item.
        - name__contains (query): File name contains filter.
        - notes__contains (query): Notes filter.
        - size__lte (query): Maximum file size.
        - size__gte (query): Minimum file size.
        - tags (query): Exact tags filter.
        - tags__any (query): Tags filter with any tag in the list.
        - tags__contains (query): Tags filter.
        - include (query): The the fields you want included in the response. If not specified, the response includes a default set of fields specific to this method. For development you can use the special value * to return all fields, but you will achieve greater performance by only selecting the fields you need.
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
    endpoint = "/downloads"
    params = {}
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    if mimeType is not None:
        params['mimeType'] = mimeType
    if mimeType__contains is not None:
        params['mimeType__contains'] = mimeType__contains
    if createTimestamp__lte is not None:
        params['createTimestamp__lte'] = createTimestamp__lte
    if createTimestamp__gte is not None:
        params['createTimestamp__gte'] = createTimestamp__gte
    if expireTimestamp__lte is not None:
        params['expireTimestamp__lte'] = expireTimestamp__lte
    if expireTimestamp__gte is not None:
        params['expireTimestamp__gte'] = expireTimestamp__gte
    if directory is not None:
        params['directory'] = directory
    if directory__contains is not None:
        params['directory__contains'] = directory__contains
    if name is not None:
        params['name'] = name
    if name__contains is not None:
        params['name__contains'] = name__contains
    if notes__contains is not None:
        params['notes__contains'] = notes__contains
    if size__lte is not None:
        params['size__lte'] = size__lte
    if size__gte is not None:
        params['size__gte'] = size__gte
    if tags is not None:
        params['tags'] = tags
    if tags__any is not None:
        params['tags__any'] = tags__any
    if tags__contains is not None:
        params['tags__contains'] = tags__contains
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


def get_download(self, id, include=None):
    """Auto-generated method for 'getDownload'

    Gets details of a download based on its ID.

    HTTP Method: GET
    Endpoint: /downloads/{id}

    Parameters:
        - id (path): Item ID.
        - include (query): The the fields you want included in the response. If not specified, the response includes a default set of fields specific to this method. For development you can use the special value * to return all fields, but you will achieve greater performance by only selecting the fields you need.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/downloads/{id}"
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


def update_download(self, body, id):
    """Auto-generated method for 'updateDownload'

    Modifies the details of a download.

    HTTP Method: PATCH
    Endpoint: /downloads/{id}

    Parameters:
        - id (path): Item ID.

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - id (string): The ID of the download.
        - directory (string): Name of the parent directory.
        - mimeType (string): The media content type.
        - name (string): Name of the item.
        - expireTimestamp (string): No description provided.
        - md5 (string): MD5 hash of the file.
        - createTimestamp (string): Date and time when the download was created.
        - updateTimestamp (string): Date and time when the download was created.
        - notes (string): User entered annotations.
        - size (integer): Size of the file in Bytes.
        - tags (array): List of tags associated with the item.
        - details (object): No description provided.

    Responses:
        - 204: Download metadata updated.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = f"/downloads/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def download_download(self, id):
    """Auto-generated method for 'downloadDownload'

    Save a download by ID.

    HTTP Method: GET
    Endpoint: /downloads/{id}:download

    Parameters:
        - id (path): Item ID.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/downloads/{id}:download"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
