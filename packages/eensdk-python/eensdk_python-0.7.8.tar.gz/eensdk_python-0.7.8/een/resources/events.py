def create_event(self, body=None):
    """Auto-generated method for 'createEvent'

    Creates a new event and adds it to the history of the selected camera. The event must be from the list of [supported event types](https://developer.eagleeyenetworks.com/docs/event-type). For more information, please review the [Event Insertion Guide](doc:event-insertion).

    HTTP Method: POST
    Endpoint: /events

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Responses:
        - 201: Event created
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/events"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_events(self, startTimestamp__gte, actor, type__in, pageToken=None, pageSize=None, include=None, startTimestamp__lte=None, endTimestamp__lte=None, endTimestamp__gte=None):
    """Auto-generated method for 'listEvents'

    Gets all events of a specified type attributed to a specific actor such as a device, user, etc. By default, the API will return only the general event information. To include additional data specific to the requested event type, use the include parameter. The possible values for the include parameter are returned in the dataSchemas field of the event object.


    HTTP Method: GET
    Endpoint: /events

    Parameters:
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - include (query): List of properties that should be included in the response. The `data` field must be included as a prefix to request the desired data. For example, if the client wants to have object detection details and supports the `een.objectDetection.v1` schemas, it can add `data.een.objectDetection.v1` to the list of requested includes. The list of supported schemas can be found in the `dataSchemas` field of the event.

        - startTimestamp__lte (query): Filter to get only events that have a `startTimestamp` value that is less than or equal to the given value. If endTimestamp__lte is not provided, this parameter is required.
        - startTimestamp__gte (query): Filter to get only events that have a `startTimestamp` value that is more than or equal to the given value.
        - endTimestamp__lte (query): Filter to get only events that have an `endTimestamp` value that is less than or equal to the given value. If startTimestamp__lte is not provided, this parameter is required.
        - endTimestamp__gte (query): Filter to get only events that have an `endTimestamp` value that is more than or equal to the given value.
        - actor (query): Filter to get only events that have an actorType and actorId value that equals the given value. The actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to filter for events for a camera with id `100d4c41`, the actor that has to be used is `camera:100d4c41`.

        - type__in (query): Filter to get only events that have a `type` value that equals one of the given parameter values. The set of all possible types can be found using the [`/eventTypes`](ref:listeventtypes) API. To get the list of event types that have been recorded for a specific actor/device, use [`/events:listFieldValues`](ref:listeventsfieldvalues).


    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 500: No description provided
    """
    endpoint = "/events"
    params = {}
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if startTimestamp__lte is not None:
        params['startTimestamp__lte'] = startTimestamp__lte
    if startTimestamp__gte is not None:
        params['startTimestamp__gte'] = startTimestamp__gte
    if endTimestamp__lte is not None:
        params['endTimestamp__lte'] = endTimestamp__lte
    if endTimestamp__gte is not None:
        params['endTimestamp__gte'] = endTimestamp__gte
    if actor is not None:
        params['actor'] = actor
    if type__in is not None:
        if isinstance(type__in, list):
            params['type__in'] = ','.join(map(str, type__in))
        else:
            params['type__in'] = str(type__in)
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def list_events_field_values(self, actor):
    """Auto-generated method for 'listEventsFieldValues'

    Retrieves the available values for each field. It is useful to know which filters to use when searching for events.

    HTTP Method: GET
    Endpoint: /events:listFieldValues

    Parameters:
        - actor (query): Filter to get available values for fields only for events that have an actorType and actorId value that equals the given value. The actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to filter for fields for a camera with id `100d4c41`, the actor that has to be used is `camera:100d4c41`.


    Responses:
        - 200: Success, lists field values as populated in the events.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/events:listFieldValues"
    params = {}
    if actor is not None:
        params['actor'] = actor
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def list_event_types(self, language=None):
    """Auto-generated method for 'listEventTypes'

    Fetches all the event types that are currently supported.

    HTTP Method: GET
    Endpoint: /eventTypes

    Parameters:
        - unknown (None): No description provided
        - Accept-Language (header): Allows clients to request translated versions of human readable fields such as the `name` and `description` fields. If no translation is available, the values will be returned in English. If both the `Accept-Language` and `language=` query parameter are used, the query parameter value is used and the header is ignored.

        - language (query): Allows clients to request translated versions of human readable fields such as the `name` and `description` fields. If no translation is available, the values will be returned in English. If both the `Accept-Language` and `language=` query parameter are used, the query parameter value is used and the header is ignored.


    Responses:
        - 200: Success, lists field values as populated in the events.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/eventTypes"
    params = {}
    if language is not None:
        params['language'] = language
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
