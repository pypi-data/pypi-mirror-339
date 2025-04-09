def get_files(self, sort=None, mimeType=None, mimeType__contains=None, createTimestamp__lte=None, createTimestamp__gte=None, directory=None, directory__contains=None, name=None, name__contains=None, notes__contains=None, size__lte=None, size__gte=None, include=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'getFiles'

    Returns a list of archived items.

    HTTP Method: GET
    Endpoint: /files

    Parameters:
        - sort (query): List of fields that should be sorted. Use "-" and the field name to specify descending results. Use "+" and the field name to specify ascending results. By default, results are sorted by create timestamp in ascending order.
        - mimeType (query): Exact content type.
        - mimeType__contains (query): Content type contains filter.
        - createTimestamp__lte (query): Maximum timestamp for file creation date.
        - createTimestamp__gte (query): Minimum timestamp for file creation date.
        - directory (query): Name of parent directory.
        - directory__contains (query): Item directory contains filter.
        - name (query): Exact name of the item.
        - name__contains (query): File name contains filter.
        - notes__contains (query): Notes filter.
        - size__lte (query): Maximum file size.
        - size__gte (query): Minimum file size.
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
    endpoint = "/files"
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


def add_file(self, name=None, directory=None, mimeType=None, body=None):
    """Auto-generated method for 'addFile'

    Add a new file to the archive. If the directory specified does not exist, it will automatically be created. To create a new empty directory, specify the desired name, parent directory and a mimeType of `application/directory`.

    HTTP Method: POST
    Endpoint: /files

    Parameters:
        - name (query): Exact name of the item.
        - directory (query): Name of parent directory.
        - mimeType (query): Exact content type.

    Request Body:
        - body (application/octet-stream):
            Description: 
            Required: False

    Responses:
        - 201: Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = "/files"
    params = {}
    if name is not None:
        params['name'] = name
    if directory is not None:
        params['directory'] = directory
    if mimeType is not None:
        params['mimeType'] = mimeType
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_file(self, id, include=None):
    """Auto-generated method for 'getFile'

    Gets details of a file based on its ID.

    HTTP Method: GET
    Endpoint: /files/{id}

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
    endpoint = f"/files/{id}"
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


def update_file(self, body, id):
    """Auto-generated method for 'updateFile'

    Modifies the details of an item.

    HTTP Method: PATCH
    Endpoint: /files/{id}

    Parameters:
        - id (path): Item ID.

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - id (string): The ID of the item.
        - directory (string): Name of the parent directory.
        - mimeType (string): The media content type.
        - name (string): Name of the item.
        - accountId (string): The account ID of the item.
        - createTimestamp (string): Date and time when the item was created.
        - updateTimestamp (string): Date and time when the item was created.
        - size (integer): Size of the file in Bytes.
        - tags (array): Tags for the file.
        - publicShare (object): Public share properties.
        - notes (string): User entered annotations.
        - details (object): No description provided.

    Responses:
        - 204: File Updated.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: No description provided
        - 500: No description provided
    """
    endpoint = f"/files/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_file(self, id):
    """Auto-generated method for 'deleteFile'

    Recycles an item by ID.

    HTTP Method: DELETE
    Endpoint: /files/{id}

    Parameters:
        - id (path): Item ID.

    Responses:
        - 204: File moved to recycle bin.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/files/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def download_file(self, id):
    """Auto-generated method for 'downloadFile'

    Download file or folder by ID.

    HTTP Method: GET
    Endpoint: /files/{id}:download

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
    endpoint = f"/files/{id}:download"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_trash(self, sort=None, mimeType=None, mimeType__contains=None, createTimestamp__lte=None, createTimestamp__gte=None, name=None, name__contains=None):
    """Auto-generated method for 'getTrash'

    Returns a list of deleted files.

    HTTP Method: GET
    Endpoint: /deletedFiles

    Parameters:
        - sort (query): List of fields that should be sorted. Use "-" and the field name to specify descending results. Use "+" and the field name to specify ascending results. By default, results are sorted by create timestamp in ascending order.
        - mimeType (query): Exact content type.
        - mimeType__contains (query): Content type contains filter.
        - createTimestamp__lte (query): Maximum timestamp for file creation date.
        - createTimestamp__gte (query): Minimum timestamp for file creation date.
        - name (query): Exact name of the item.
        - name__contains (query): File name contains filter.
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/deletedFiles"
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
    if name is not None:
        params['name'] = name
    if name__contains is not None:
        params['name__contains'] = name__contains
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_trash_file(self, id):
    """Auto-generated method for 'getTrashFile'

    Get details of a recycled item.

    HTTP Method: GET
    Endpoint: /deletedFiles/{id}

    Parameters:
        - id (path): Item ID.

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: No description provided
        - 500: No description provided
    """
    endpoint = f"/deletedFiles/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_trash_file(self, id):
    """Auto-generated method for 'deleteTrashFile'

    Permanently delete an item by ID.

    HTTP Method: DELETE
    Endpoint: /deletedFiles/{id}

    Parameters:
        - id (path): Item ID.

    Responses:
        - 204: File deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/deletedFiles/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def delete_all_trash_files(self):
    """Auto-generated method for 'deleteAllTrashFiles'

    Permanently delete all files in the recycle bin.

    HTTP Method: DELETE
    Endpoint: /deletedFiles/all

    Responses:
        - 204: Permanently delete all files in the recycle bin.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/deletedFiles/all"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def restore_trash_file(self, id):
    """Auto-generated method for 'restoreTrashFile'

    Restore a recycled item by ID.

    HTTP Method: POST
    Endpoint: /deletedFiles/{id}:restore

    Parameters:
        - id (path): Item ID.

    Responses:
        - 201: File restored.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/deletedFiles/{id}:restore"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
