def list_alerts(self, language=None, creatorId=None, timestamp__lte=None, timestamp__gte=None, alertType__in=None, actorId__in=None, actorType=None, actorAccountId=None, ruleId=None, eventId=None, locationId__in=None, include=None, sort=None):
    """Auto-generated method for 'listAlerts'

    Search and sort alerts by creatorId, alertType, actorId, actorType, actorAccountId, ruleId, eventId, locationId, and priority. Optional information can be requested with include.


    HTTP Method: GET
    Endpoint: /alerts

    Parameters:
        - Accept-Language (header): No description provided
        - language (query): Language query overrides Accept-Language header
        - creatorId (query): Filter by creatorId
        - timestamp__lte (query): Filter by timestamp__lte
        - timestamp__gte (query): Filter by timestamp__gte
        - alertType__in (query): Filter by alertType (supports multiple values)
        - actorId__in (query): Filter by actorId (supports multiple values)
        - actorType (query): Filter by actorType
        - actorAccountId (query): Filter by actorAccountId
        - ruleId (query): Filter by ruleId
        - eventId (query): Filter by eventId
        - locationId__in (query): Filter by one or more location IDs.
        - unknown (None): No description provided
        - include (query): Specify additional data to include in the response (supports multiple values like `data` and `actions`).
        - sort (query): Sort by timestamp

    Responses:
        - 200: Alert results
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/alerts"
    params = {}
    if language is not None:
        params['language'] = language
    if creatorId is not None:
        params['creatorId'] = creatorId
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if alertType__in is not None:
        if isinstance(alertType__in, list):
            params['alertType__in'] = ','.join(map(str, alertType__in))
        else:
            params['alertType__in'] = str(alertType__in)
    if actorId__in is not None:
        if isinstance(actorId__in, list):
            params['actorId__in'] = ','.join(map(str, actorId__in))
        else:
            params['actorId__in'] = str(actorId__in)
    if actorType is not None:
        params['actorType'] = actorType
    if actorAccountId is not None:
        params['actorAccountId'] = actorAccountId
    if ruleId is not None:
        params['ruleId'] = ruleId
    if eventId is not None:
        params['eventId'] = eventId
    if locationId__in is not None:
        if isinstance(locationId__in, list):
            params['locationId__in'] = ','.join(map(str, locationId__in))
        else:
            params['locationId__in'] = str(locationId__in)
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
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_alert(self, id):
    """Auto-generated method for 'getAlert'

    Get an alert


    HTTP Method: GET
    Endpoint: /alerts/{id}

    Parameters:
        - id (path): Alert id

    Responses:
        - 200: Alert result
        - 401: No description provided
        - 403: No description provided
        - 404: Referenced resource could not be found.
        - 500: No description provided
    """
    endpoint = f"/alerts/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
