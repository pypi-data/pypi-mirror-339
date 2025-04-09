def list_event_subscriptions(self, pageToken=None, pageSize=None):
    """Auto-generated method for 'listEventSubscriptions'

    Gets all visible event subscriptions defined for the current account.

    HTTP Method: GET
    Endpoint: /eventSubscriptions

    Parameters:
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/eventSubscriptions"
    params = {}
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


def create_event_subscription(self, body=None):
    """Auto-generated method for 'createEventSubscription'

    Creates a new event subscription.

    HTTP Method: POST
    Endpoint: /eventSubscriptions

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - deliveryConfig (object): Describes how the event subscription should deliver events to the client.
        - filters (array): Optional list of filters that should be added to the event subscription from the moment of creation.


    Responses:
        - 201: EventSubscription created
        - 400: No description provided
        - 401: No description provided
        - 404: Referenced resource could not be found.
        - 500: No description provided
    """
    endpoint = "/eventSubscriptions"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_event_subscription(self, eventSubscriptionId):
    """Auto-generated method for 'getEventSubscription'

    This endpoint allows you to retrieve a specific event subscription.

    HTTP Method: GET
    Endpoint: /eventSubscriptions/{eventSubscriptionId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_event_subscription(self, eventSubscriptionId):
    """Auto-generated method for 'deleteEventSubscription'

    Deletes a specific event subscription.

    HTTP Method: DELETE
    Endpoint: /eventSubscriptions/{eventSubscriptionId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID

    Responses:
        - 204: EventSubscription deleted
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def list_event_subscription_filters(self, eventSubscriptionId):
    """Auto-generated method for 'listEventSubscriptionFilters'

    Gets all event subscription filters defined for the given event subscription.

    HTTP Method: GET
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_event_subscription_filter(self, eventSubscriptionId, body=None):
    """Auto-generated method for 'createEventSubscriptionFilter'

    Creates an event subscription filter for a given event subscription.

    HTTP Method: POST
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - actors (array): List of actors for which events should be delivered to this event subscription.
        - types (array): List of event types of which events should be delivered to this event subscription.

    Responses:
        - 201: Filter created
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_event_subscription_filter(self, eventSubscriptionId, filterId):
    """Auto-generated method for 'getEventSubscriptionFilter'

    Gets info about a specific filter of a given event subscription ID.

    HTTP Method: GET
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters/{filterId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID
        - filterId (path): Event Subscription Filter ID

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters/{filterId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def delete_event_subscription_filter(self, eventSubscriptionId, filterId):
    """Auto-generated method for 'deleteEventSubscriptionFilter'

    Deletes a filter based on the given ID.

    HTTP Method: DELETE
    Endpoint: /eventSubscriptions/{eventSubscriptionId}/filters/{filterId}

    Parameters:
        - eventSubscriptionId (path): Event Subscription ID
        - filterId (path): Event Subscription Filter ID

    Responses:
        - 204: Filter deleted
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/eventSubscriptions/{eventSubscriptionId}/filters/{filterId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
