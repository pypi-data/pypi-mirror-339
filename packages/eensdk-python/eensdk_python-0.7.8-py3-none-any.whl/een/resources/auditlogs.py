def list_auditlogs(self, timestamp__gte, timestamp__lte, include=None, userId=None, targetId=None, targetType=None, locationId=None, auditType=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'listAuditlogs'

    This endpoint filters audit events by userId, targetId, targetType, auditType


    HTTP Method: GET
    Endpoint: /auditLogs

    Parameters:
        - include (query): No description provided
        - userId (query): Filter by userId
        - targetId (query): Filter by targetId
        - targetType (query): Filter by targetType
        - locationId (query): Filter by locationId
        - auditType (query): Filter by auditType
        - timestamp__gte (query): Minimum timestamp to list auditlogs.
        - timestamp__lte (query): Maximum timestamp to list auditlogs.
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: List of audit events
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/auditLogs"
    params = {}
    if include is not None:
        params['include'] = include
    if userId is not None:
        params['userId'] = userId
    if targetId is not None:
        params['targetId'] = targetId
    if targetType is not None:
        params['targetType'] = targetType
    if locationId is not None:
        params['locationId'] = locationId
    if auditType is not None:
        params['auditType'] = auditType
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
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
