def parse_video_analytics(self, language=None, body=None):
    """Auto-generated method for 'parseVideoAnalytics'

    Map a natural language query to a set of object filters to use in the deep search endpoints. The
deep search can identify a variety of objects, including people, vehicles, and some common handheld
objects such as backpacks and suitcases. The deep search can also identify the attributes of these
objects, such as the color of a person's clothing or the make of a vehicle.

    HTTP Method: POST
    Endpoint: /videoAnalyticEvents:parse

    Parameters:
        - Accept-Language (header): Allows clients to request translated versions of human readable fields such as the `name` and `description` fields. If no translation is available, the values will be returned in English. If both the `Accept-Language` and `language=` query parameter are used, the query parameter value is used and the header is ignored.

        - language (query): Allows clients to request translated versions of human readable fields such as the `name` and `description` fields. If no translation is available, the values will be returned in English. If both the `Accept-Language` and `language=` query parameter are used, the query parameter value is used and the header is ignored.


    Request Body:
        - body (application/json):
            Description: Pass the query string that is to be converted
            Required: False

    Top-level Request Body Properties:
        - query (string): A natural language query for searching events based on their metadata.

    Responses:
        - 200: No description provided
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/videoAnalyticEvents:parse"
    params = {}
    if language is not None:
        params['language'] = language
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_video_analytics_events(self, timestamp__gte, timestamp__lte, actor__in=None, layoutId__in=None, tags__any=None, roiName__in=None, creatorId__in=None, eventType__in=None, pageToken=None, pageSize=None, include=None, sort=None, body=None):
    """Auto-generated method for 'listVideoAnalyticsEvents'

    Fetches video analytic events matching the filters defined for the deep search. The events are returned as the base event envelope with the data objects requested using the `include` parameter.

    HTTP Method: POST
    Endpoint: /videoAnalyticEvents:deepSearch

    Parameters:
        - timestamp__gte (query): Minimum range of timestamp to fetch events after this time. Default would be 2 hours from current time.
        - timestamp__lte (query): Maximum range of timestamp to fetch events before this time. Default would be the current time.
        - actor__in (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list.
The `actorType` must be prefixed to the `actorId` using a colon (`:`) separator.
For example:
- To filter for a camera with ID `cameraId_1`, use `camera:cameraId_1`.
- To filter for a location with ID `locationId_1`, use `location:locationId_1`.
- To filter for a bridge with ID `bridgeId_1`, use `bridge:bridgeId_1`.

Currently, the following `actorType` values are supported:
- `camera`: Matches the specific camera ID.
- `location`: Matches all camera IDs associated with the specified location ID(s).
- `bridge`: Matches all camera IDs associated with the specified bridge ID(s).

If multiple actor types are provided (e.g., `camera`, `location`, and `bridge`), the filter will include camera IDs associated with **any** of the given values.
        - layoutId__in (query): Filter to get only events associated with camera Ids mapped to the specified layout Ids.
Accepts a comma-separated list of layout Ids (e.g., `layoutId_1,layoutId_2`).
All matching camera IDs for the provided layout IDs will be included in the result.
        - tags__any (query): Filter to get only events associated with camera Ids mapped to the specified tag Ids.
Accepts a comma-separated list of tag Ids (e.g., `tagId_1,tagId_2`).
All matching camera IDs for the provided tag IDs will be included in the result.
Here the suffix `__any` is used to indicate that the filter is an OR operation, i.e., events associated with any of the provided tag IDs will be included in the result.
        - roiName__in (query): Matches with all events that have at least one motion-event related region with a name containing one or more of the values in this list. Matching is done exactly but is not case-sensitive.
        - creatorId__in (query): Filter to get only events that have a `creatorId` value that equals one of the given parameter values.

To get the list of creatorIds that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - eventType__in (query): Filter to get only events that have a `type` value that equals one of the given parameter values.

To get the list of event types that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - include (query): List of properties that should be included in the response, if available.
The `data` field can be used as prefix to request data if it is available.
Eg. if the client wants to have object detection details and supports the
`een.objectDetection.v1` schemas, it can add `data.een.objectDetection.v1` to the list of requested includes.
This parameter does not operate as a filter, events without the requested properties are still returned.
        - sort (query): Provide options to sort in ascending or descending order based on timestamp

    Request Body:
        - body (application/json):
            Description: The request body can be used to add additional object details based on various combinations of the object metadata.
            Required: False

    Responses:
        - 200: No description provided
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/videoAnalyticEvents:deepSearch"
    params = {}
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if actor__in is not None:
        if isinstance(actor__in, list):
            params['actor__in'] = ','.join(map(str, actor__in))
        else:
            params['actor__in'] = str(actor__in)
    if layoutId__in is not None:
        params['layoutId__in'] = layoutId__in
    if tags__any is not None:
        params['tags__any'] = tags__any
    if roiName__in is not None:
        params['roiName__in'] = roiName__in
    if creatorId__in is not None:
        if isinstance(creatorId__in, list):
            params['creatorId__in'] = ','.join(map(str, creatorId__in))
        else:
            params['creatorId__in'] = str(creatorId__in)
    if eventType__in is not None:
        if isinstance(eventType__in, list):
            params['eventType__in'] = ','.join(map(str, eventType__in))
        else:
            params['eventType__in'] = str(eventType__in)
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if sort is not None:
        params['sort'] = sort
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_video_analytics_events_deep_search_group_by_resource(self, timestamp__gte, timestamp__lte, actor__in=None, layoutId__in=None, tags__any=None, roiName__in=None, creatorId__in=None, eventType__in=None, include=None, sort=None, groupBy=None, body=None):
    """Auto-generated method for 'listVideoAnalyticsEventsDeepSearchGroupByResource'

    Fetches matching video analytic event frequencies grouped as requested. The response is a list of groups, each with a count of matching events, and optionally a sample event.

    HTTP Method: POST
    Endpoint: /videoAnalyticEvents:deepSearchGroupByResource

    Parameters:
        - timestamp__gte (query): Minimum range of timestamp to fetch events after this time. Default would be 2 hours from current time.
        - timestamp__lte (query): Maximum range of timestamp to fetch events before this time. Default would be the current time.
        - actor__in (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list.
The `actorType` must be prefixed to the `actorId` using a colon (`:`) separator.
For example:
- To filter for a camera with ID `cameraId_1`, use `camera:cameraId_1`.
- To filter for a location with ID `locationId_1`, use `location:locationId_1`.
- To filter for a bridge with ID `bridgeId_1`, use `bridge:bridgeId_1`.

Currently, the following `actorType` values are supported:
- `camera`: Matches the specific camera ID.
- `location`: Matches all camera IDs associated with the specified location ID(s).
- `bridge`: Matches all camera IDs associated with the specified bridge ID(s).

If multiple actor types are provided (e.g., `camera`, `location`, and `bridge`), the filter will include camera IDs associated with **any** of the given values.
        - layoutId__in (query): Filter to get only events associated with camera Ids mapped to the specified layout Ids.
Accepts a comma-separated list of layout Ids (e.g., `layoutId_1,layoutId_2`).
All matching camera IDs for the provided layout IDs will be included in the result.
        - tags__any (query): Filter to get only events associated with camera Ids mapped to the specified tag Ids.
Accepts a comma-separated list of tag Ids (e.g., `tagId_1,tagId_2`).
All matching camera IDs for the provided tag IDs will be included in the result.
Here the suffix `__any` is used to indicate that the filter is an OR operation, i.e., events associated with any of the provided tag IDs will be included in the result.
        - roiName__in (query): Matches with all events that have at least one motion-event related region with a name containing one or more of the values in this list. Matching is done exactly but is not case-sensitive.
        - creatorId__in (query): Filter to get only events that have a `creatorId` value that equals one of the given parameter values.

To get the list of creatorIds that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - eventType__in (query): Filter to get only events that have a `type` value that equals one of the given parameter values.

To get the list of event types that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - unknown (None): No description provided
        - include (query): List of properties that should be included in the response, if available.
The `data` field can be used as prefix to request data if it is available.
Eg. if the client wants to have object detection details and supports the
`een.objectDetection.v1` schemas, it can add `data.een.objectDetection.v1` to the list of requested includes.
This parameter does not operate as a filter, events without the requested properties are still returned.
        - sort (query): Provide options to sort in ascending or descending order based on timestamp/events count/alphabetical order
        - groupBy (query): Contains the information on the event metadata on which the grouping has to be executed. Currently supports `camera` based grouping only

    Request Body:
        - body (application/json):
            Description: The request body can be used to add additional object details based on various combinations of the object metadata.
            Required: False

    Responses:
        - 200: No description provided
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/videoAnalyticEvents:deepSearchGroupByResource"
    params = {}
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if actor__in is not None:
        if isinstance(actor__in, list):
            params['actor__in'] = ','.join(map(str, actor__in))
        else:
            params['actor__in'] = str(actor__in)
    if layoutId__in is not None:
        params['layoutId__in'] = layoutId__in
    if tags__any is not None:
        params['tags__any'] = tags__any
    if roiName__in is not None:
        params['roiName__in'] = roiName__in
    if creatorId__in is not None:
        if isinstance(creatorId__in, list):
            params['creatorId__in'] = ','.join(map(str, creatorId__in))
        else:
            params['creatorId__in'] = str(creatorId__in)
    if eventType__in is not None:
        if isinstance(eventType__in, list):
            params['eventType__in'] = ','.join(map(str, eventType__in))
        else:
            params['eventType__in'] = str(eventType__in)
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if sort is not None:
        params['sort'] = sort
    if groupBy is not None:
        params['groupBy'] = groupBy
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_video_analytics_events_deep_search_group_by_time(self, timestamp__gte, timestamp__lte, actor__in=None, layoutId__in=None, tags__any=None, roiName__in=None, creatorId__in=None, eventType__in=None, include=None, sort=None, timeInterval=None, groupCount=None, body=None):
    """Auto-generated method for 'listVideoAnalyticsEventsDeepSearchGroupByTime'

    Fetches matching video analytic event frequencies grouped in time periods.
The set of periods are defined by defining either their length using `timeInterval`, or their count with `groupCount`.
The response is a list of time periods, each with a count of matching events, and optionally a sample event.

    HTTP Method: POST
    Endpoint: /videoAnalyticEvents:deepSearchGroupByTime

    Parameters:
        - timestamp__gte (query): Minimum range of timestamp to fetch events after this time. Default would be 2 hours from current time.
        - timestamp__lte (query): Maximum range of timestamp to fetch events before this time. Default would be the current time.
        - actor__in (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list.
The `actorType` must be prefixed to the `actorId` using a colon (`:`) separator.
For example:
- To filter for a camera with ID `cameraId_1`, use `camera:cameraId_1`.
- To filter for a location with ID `locationId_1`, use `location:locationId_1`.
- To filter for a bridge with ID `bridgeId_1`, use `bridge:bridgeId_1`.

Currently, the following `actorType` values are supported:
- `camera`: Matches the specific camera ID.
- `location`: Matches all camera IDs associated with the specified location ID(s).
- `bridge`: Matches all camera IDs associated with the specified bridge ID(s).

If multiple actor types are provided (e.g., `camera`, `location`, and `bridge`), the filter will include camera IDs associated with **any** of the given values.
        - layoutId__in (query): Filter to get only events associated with camera Ids mapped to the specified layout Ids.
Accepts a comma-separated list of layout Ids (e.g., `layoutId_1,layoutId_2`).
All matching camera IDs for the provided layout IDs will be included in the result.
        - tags__any (query): Filter to get only events associated with camera Ids mapped to the specified tag Ids.
Accepts a comma-separated list of tag Ids (e.g., `tagId_1,tagId_2`).
All matching camera IDs for the provided tag IDs will be included in the result.
Here the suffix `__any` is used to indicate that the filter is an OR operation, i.e., events associated with any of the provided tag IDs will be included in the result.
        - roiName__in (query): Matches with all events that have at least one motion-event related region with a name containing one or more of the values in this list. Matching is done exactly but is not case-sensitive.
        - creatorId__in (query): Filter to get only events that have a `creatorId` value that equals one of the given parameter values.

To get the list of creatorIds that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - eventType__in (query): Filter to get only events that have a `type` value that equals one of the given parameter values.

To get the list of event types that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - unknown (None): No description provided
        - include (query): List of properties that should be included in the response, if available.
The `data` field can be used as prefix to request data if it is available.
Eg. if the client wants to have object detection details and supports the
`een.objectDetection.v1` schemas, it can add `data.een.objectDetection.v1` to the list of requested includes.
This parameter does not operate as a filter, events without the requested properties are still returned.
        - sort (query): Provide options to sort in ascending or descending order based on timestamp/events count/alphabetical order
        - timeInterval (query): The time interval of each of time-based groups.
The values can be numbers followed by s(seconds)/m(minutes)/h(hours)/d(days).
Example: 10s, 20m etc

**Note:** It is mandatory to have either of `timeInterval` or `groupCount` query parameter.
Presence of none or presence of both would return a 400 status code.
        - groupCount (query): Total number of time-based groups.
The total time between `timestamp__lte` and `timestamp__gte` gets evenly distributed across all the groups

**Note:** It is mandatory to have either of `timeInterval` or `groupCount` query parameter.
Presence of none or presence of both would return a 400 status code.

    Request Body:
        - body (application/json):
            Description: The request body can be used to add additional object details based on various combinations of the object metadata.
            Required: False

    Responses:
        - 200: No description provided
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/videoAnalyticEvents:deepSearchGroupByTime"
    params = {}
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if actor__in is not None:
        if isinstance(actor__in, list):
            params['actor__in'] = ','.join(map(str, actor__in))
        else:
            params['actor__in'] = str(actor__in)
    if layoutId__in is not None:
        params['layoutId__in'] = layoutId__in
    if tags__any is not None:
        params['tags__any'] = tags__any
    if roiName__in is not None:
        params['roiName__in'] = roiName__in
    if creatorId__in is not None:
        if isinstance(creatorId__in, list):
            params['creatorId__in'] = ','.join(map(str, creatorId__in))
        else:
            params['creatorId__in'] = str(creatorId__in)
    if eventType__in is not None:
        if isinstance(eventType__in, list):
            params['eventType__in'] = ','.join(map(str, eventType__in))
        else:
            params['eventType__in'] = str(eventType__in)
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if sort is not None:
        params['sort'] = sort
    if timeInterval is not None:
        params['timeInterval'] = timeInterval
    if groupCount is not None:
        params['groupCount'] = groupCount
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_video_analytics_field_values(self, timestamp__gte, timestamp__lte, parameter, actor__in=None, layoutId__in=None, tags__any=None, roiName__in=None, creatorId__in=None, eventType__in=None, body=None):
    """Auto-generated method for 'listVideoAnalyticsFieldValues'

    Fetches available deep search query parameters based on events matching the input filters and other query parameter inputs.
Query parameters can be requested using the `parameter` param.
It has to be noted that the values in the filter will be a subset for those fields which are mentioned in the `parameter` param.
Eg. If the filter specifies a set of actors (such as cameras), and `parameter=actor` is given, the search for matching is done with the given actor filters and therefore the response will always be a subset of the given list of actors.

    HTTP Method: POST
    Endpoint: /videoAnalyticEvents:listFieldValues

    Parameters:
        - timestamp__gte (query): Minimum range of timestamp to fetch events after this time. Default would be 2 hours from current time.
        - timestamp__lte (query): Maximum range of timestamp to fetch events before this time. Default would be the current time.
        - actor__in (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list.
The `actorType` must be prefixed to the `actorId` using a colon (`:`) separator.
For example:
- To filter for a camera with ID `cameraId_1`, use `camera:cameraId_1`.
- To filter for a location with ID `locationId_1`, use `location:locationId_1`.
- To filter for a bridge with ID `bridgeId_1`, use `bridge:bridgeId_1`.

Currently, the following `actorType` values are supported:
- `camera`: Matches the specific camera ID.
- `location`: Matches all camera IDs associated with the specified location ID(s).
- `bridge`: Matches all camera IDs associated with the specified bridge ID(s).

If multiple actor types are provided (e.g., `camera`, `location`, and `bridge`), the filter will include camera IDs associated with **any** of the given values.
        - layoutId__in (query): Filter to get only events associated with camera Ids mapped to the specified layout Ids.
Accepts a comma-separated list of layout Ids (e.g., `layoutId_1,layoutId_2`).
All matching camera IDs for the provided layout IDs will be included in the result.
        - tags__any (query): Filter to get only events associated with camera Ids mapped to the specified tag Ids.
Accepts a comma-separated list of tag Ids (e.g., `tagId_1,tagId_2`).
All matching camera IDs for the provided tag IDs will be included in the result.
Here the suffix `__any` is used to indicate that the filter is an OR operation, i.e., events associated with any of the provided tag IDs will be included in the result.
        - roiName__in (query): Matches with all events that have at least one motion-event related region with a name containing one or more of the values in this list. Matching is done exactly but is not case-sensitive.
        - creatorId__in (query): Filter to get only events that have a `creatorId` value that equals one of the given parameter values.

To get the list of creatorIds that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - eventType__in (query): Filter to get only events that have a `type` value that equals one of the given parameter values.

To get the list of event types that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - parameter (query): Provide the parameter to be returned in the response body with the list of available values for the selected parameter.

    Request Body:
        - body (application/json):
            Description: The request body can be used to add additional object details based on various combinations of the object metadata.
            Required: False

    Responses:
        - 200: List of field values matching search criteria
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/videoAnalyticEvents:listFieldValues"
    params = {}
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if actor__in is not None:
        if isinstance(actor__in, list):
            params['actor__in'] = ','.join(map(str, actor__in))
        else:
            params['actor__in'] = str(actor__in)
    if layoutId__in is not None:
        params['layoutId__in'] = layoutId__in
    if tags__any is not None:
        params['tags__any'] = tags__any
    if roiName__in is not None:
        params['roiName__in'] = roiName__in
    if creatorId__in is not None:
        if isinstance(creatorId__in, list):
            params['creatorId__in'] = ','.join(map(str, creatorId__in))
        else:
            params['creatorId__in'] = str(creatorId__in)
    if eventType__in is not None:
        if isinstance(eventType__in, list):
            params['eventType__in'] = ','.join(map(str, eventType__in))
        else:
            params['eventType__in'] = str(eventType__in)
    if parameter is not None:
        params['parameter'] = parameter
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_video_analytics_object_values(self, timestamp__gte, timestamp__lte, actor__in=None, layoutId__in=None, tags__any=None, roiName__in=None, creatorId__in=None, eventType__in=None, include=None):
    """Auto-generated method for 'listVideoAnalyticsObjectValues'

    Fetches available deep search filter attribute values for a given filter based on events matching the input filters.
The `include` parameter is used to indicate what filter the attribute values should be returned for.

    HTTP Method: GET
    Endpoint: /videoAnalyticEvents:listObjectValues

    Parameters:
        - timestamp__gte (query): Minimum range of timestamp to fetch events after this time. Default would be 2 hours from current time.
        - timestamp__lte (query): Maximum range of timestamp to fetch events before this time. Default would be the current time.
        - actor__in (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list.
The `actorType` must be prefixed to the `actorId` using a colon (`:`) separator.
For example:
- To filter for a camera with ID `cameraId_1`, use `camera:cameraId_1`.
- To filter for a location with ID `locationId_1`, use `location:locationId_1`.
- To filter for a bridge with ID `bridgeId_1`, use `bridge:bridgeId_1`.

Currently, the following `actorType` values are supported:
- `camera`: Matches the specific camera ID.
- `location`: Matches all camera IDs associated with the specified location ID(s).
- `bridge`: Matches all camera IDs associated with the specified bridge ID(s).

If multiple actor types are provided (e.g., `camera`, `location`, and `bridge`), the filter will include camera IDs associated with **any** of the given values.
        - layoutId__in (query): Filter to get only events associated with camera Ids mapped to the specified layout Ids.
Accepts a comma-separated list of layout Ids (e.g., `layoutId_1,layoutId_2`).
All matching camera IDs for the provided layout IDs will be included in the result.
        - tags__any (query): Filter to get only events associated with camera Ids mapped to the specified tag Ids.
Accepts a comma-separated list of tag Ids (e.g., `tagId_1,tagId_2`).
All matching camera IDs for the provided tag IDs will be included in the result.
Here the suffix `__any` is used to indicate that the filter is an OR operation, i.e., events associated with any of the provided tag IDs will be included in the result.
        - roiName__in (query): Matches with all events that have at least one motion-event related region with a name containing one or more of the values in this list. Matching is done exactly but is not case-sensitive.
        - creatorId__in (query): Filter to get only events that have a `creatorId` value that equals one of the given parameter values.

To get the list of creatorIds that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - eventType__in (query): Filter to get only events that have a `type` value that equals one of the given parameter values.

To get the list of event types that have been recorded for a specific actor/device, use [`/videoAnalyticEvents:listFieldValues`](ref:listVideoAnalyticsFieldValues).
        - include (query): Provide filter names for which all the possible values of each of the attributes are to be returned in response body.
These values are from the events present in the search result based on the criteria in the query parameters.

    Responses:
        - 200: List of values for each of the attributes of the selected object class that matches the search criteria
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/videoAnalyticEvents:listObjectValues"
    params = {}
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if actor__in is not None:
        if isinstance(actor__in, list):
            params['actor__in'] = ','.join(map(str, actor__in))
        else:
            params['actor__in'] = str(actor__in)
    if layoutId__in is not None:
        params['layoutId__in'] = layoutId__in
    if tags__any is not None:
        params['tags__any'] = tags__any
    if roiName__in is not None:
        params['roiName__in'] = roiName__in
    if creatorId__in is not None:
        if isinstance(creatorId__in, list):
            params['creatorId__in'] = ','.join(map(str, creatorId__in))
        else:
            params['creatorId__in'] = str(creatorId__in)
    if eventType__in is not None:
        if isinstance(eventType__in, list):
            params['eventType__in'] = ','.join(map(str, eventType__in))
        else:
            params['eventType__in'] = str(eventType__in)
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


def get_video_analytics_event(self, id, include=None):
    """Auto-generated method for 'getVideoAnalyticsEvent'

    Fetches video analytics event based on `id` provided. The event is returned as the base event envelope with the data objects requested using the `include` parameter.

    HTTP Method: GET
    Endpoint: /videoAnalyticEvents/{id}

    Parameters:
        - id (path): Id of the event
        - include (query): List of properties that should be included in the response, if available.
The `data` field can be used as prefix to request data if it is available.
Eg. if the client wants to have object detection details and supports the
`een.objectDetection.v1` schemas, it can add `data.een.objectDetection.v1` to the list of requested includes.
This parameter does not operate as a filter, events without the requested properties are still returned.

    Responses:
        - 200: Event details
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/videoAnalyticEvents/{id}"
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
