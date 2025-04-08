def get_editions(self, accountId=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'getEditions'

    This endpoint allows you to retrieve a list of the editions that are available for your account.  
It is important to note that after using the pageSize parameter, the "totalSize" in  the response represents the total number of available editions, not the number of editions resulting from the query string.


    HTTP Method: GET
    Endpoint: /editions

    Parameters:
        - accountId (query): Account ID specified in as an ESN Type.
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: Successfully fetched
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/editions"
    params = {}
    if accountId is not None:
        params['accountId'] = accountId
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


def get_edition(self, id):
    """Auto-generated method for 'getEdition'

    This endpoint allows you to retrieve a specific edition by its ID.

    HTTP Method: GET
    Endpoint: /editions/{id}

    Parameters:
        - id (path): Edition ID

    Responses:
        - 200: Successfully authorized
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/editions/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
