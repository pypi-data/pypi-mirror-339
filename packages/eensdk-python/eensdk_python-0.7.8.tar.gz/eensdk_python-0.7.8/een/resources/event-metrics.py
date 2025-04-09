def get_event_metrics(self, actor, eventType, timestamp__lte=None, timestamp__gte=None, aggregateByMinutes=None):
    """Auto-generated method for 'getEventMetrics'

    Returns metrics data indicating the number of occurrences of a given event over time.


    HTTP Method: GET
    Endpoint: /eventMetrics

    Parameters:
        - actor (query): The actor for which the metrics are to be retrieved. The actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to get the metrics for camera with id 100d4c41, the actor that has to be used is `camera:100d4c41`.

        - timestamp__lte (query): Maximum timestamp to list metrics. Defaults to now.
        - timestamp__gte (query): Minimum timestamp to list metrics. Defaults to 7 days ago.
        - eventType (query): The type of event that will be counted. The set of all possible types can be found using the  [`/eventTypes`](ref:listeventtypes) API. Only a single event type can be specified.

        - aggregateByMinutes (query): The time interval, in minutes, for grouping the event metrics.  It specifies the granularity of the time buckets used for aggregating event metrics.  It defaults to 60 minutes (1 hour) if not specified.


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/eventMetrics"
    params = {}
    if actor is not None:
        params['actor'] = actor
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if eventType is not None:
        params['eventType'] = eventType
    if aggregateByMinutes is not None:
        params['aggregateByMinutes'] = aggregateByMinutes
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
