def list_jobs(self, userId, pageToken=None, pageSize=None, sort=None, type=None, state=None, namespace=None, createTimestamp__gte=None, createTimestamp__lte=None, updateTimestamp__gte=None, updateTimestamp__lte=None, expireTimestamp__gte=None, expireTimestamp__lte=None, state__in=None):
    """Auto-generated method for 'listJobs'

    List Jobs.  Filtering by userId, type, state namespace, createTimestamp, updateTimestamp, expireTimestamp.


    HTTP Method: GET
    Endpoint: /jobs

    Parameters:
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - sort (query): List of fields that should be sorted. Use "-" and the field name to specify descending results. Use "+" and the field name to specify ascending results.
        - userId (query): Filter by Jobs.userId.  REQUIRED.

        - type (query): Filter by Jobs.type

        - state (query): Filter by Jobs.state

        - namespace (query): Filter by Jobs.namespace

        - createTimestamp__gte (query): Minimum timestamp for creation date.
        - createTimestamp__lte (query): Maximum timestamp for creation date.
        - updateTimestamp__gte (query): Minimum timestamp for update date.
        - updateTimestamp__lte (query): Maximum timestamp for update date.
        - expireTimestamp__gte (query): Minimum timestamp for expire date.
        - expireTimestamp__lte (query): Maximum timestamp for expire date.
        - state__in (query): Filter Jobs.state to those having all given state


    Responses:
        - 200: List Jobs
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/jobs"
    params = {}
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    if userId is not None:
        params['userId'] = userId
    if type is not None:
        params['type'] = type
    if state is not None:
        params['state'] = state
    if namespace is not None:
        params['namespace'] = namespace
    if createTimestamp__gte is not None:
        params['createTimestamp__gte'] = createTimestamp__gte
    if createTimestamp__lte is not None:
        params['createTimestamp__lte'] = createTimestamp__lte
    if updateTimestamp__gte is not None:
        params['updateTimestamp__gte'] = updateTimestamp__gte
    if updateTimestamp__lte is not None:
        params['updateTimestamp__lte'] = updateTimestamp__lte
    if expireTimestamp__gte is not None:
        params['expireTimestamp__gte'] = expireTimestamp__gte
    if expireTimestamp__lte is not None:
        params['expireTimestamp__lte'] = expireTimestamp__lte
    if state__in is not None:
        params['state__in'] = state__in
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_job(self, jobId):
    """Auto-generated method for 'getJob'

    Get a single Job

    HTTP Method: GET
    Endpoint: /jobs/{jobId}

    Parameters:
        - jobId (path): No description provided

    Responses:
        - 200: Get a single Job
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: Referenced resource could not be found.
        - 500: No description provided
    """
    endpoint = f"/jobs/{jobId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_job(self, jobId):
    """Auto-generated method for 'deleteJob'

    Deletes a Job regardless of state.


    HTTP Method: DELETE
    Endpoint: /jobs/{jobId}

    Parameters:
        - jobId (path): No description provided

    Responses:
        - 204: Job deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/jobs/{jobId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
