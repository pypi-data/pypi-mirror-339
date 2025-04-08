def get_tags(self, sort=None, name__contains=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'getTags'

    Retrieves a list of all tags visible to the current user.
You can filter the result by name__contains and sort the result by sort field. Additionally, you can paginate the results by pageToken and pageSize.


    HTTP Method: GET
    Endpoint: /tags

    Parameters:
        - sort (query): List of fields that should be sorted
        - name__contains (query): Filter to get Tags whose the name contains the provided substring. The lookup is exact and case insensitive
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: Account retrieved
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/tags"
    params = {}
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    if name__contains is not None:
        params['name__contains'] = name__contains
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
