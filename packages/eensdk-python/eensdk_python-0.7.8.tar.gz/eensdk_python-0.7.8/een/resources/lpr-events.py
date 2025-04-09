def list_lpr_events(self, timestamp__gte=None, timestamp__lte=None, plateConfidence__lte=None, plate=None, plate__fuzzy=None, plate__contains=None, type__in=None, recognizedText=None, recognizedText__contains=None, recognizedText__fuzzy=None, direction__in=None, accessType__in=None, actor=None, color__in=None, make__in=None, bodyType__in=None, data_een_userData_v1=None, data_een_dotNumberRecognition_v1_regNumber=None, data_een_dotNumberRecognition_v1_regNumber__contains=None, data_een_dotNumberRecognition_v1_regNumber__fuzzy=None, data_een_truckNumberRecognition_v1_regNumber=None, data_een_truckNumberRecognition_v1_regNumber__contains=None, data_een_truckNumberRecognition_v1_regNumber__fuzzy=None, data_een_trailerNumberRecognition_v1_regNumber=None, data_een_trailerNumberRecognition_v1_regNumber__contains=None, data_een_trailerNumberRecognition_v1_regNumber__fuzzy=None, data_een_lprPlateRead_v1_plate=None, data_een_lprPlateRead_v1_plate__contains=None, data_een_lprPlateRead_v1_plate__fuzzy=None, data_een_recognizedText_v1_value=None, data_een_recognizedText_v1_value__contains=None, data_een_recognizedText_v1_value__fuzzy=None, searchRelatedEventData=None, relatedEvents_rel=None, pageToken=None, pageSize=None, include=None):
    """Auto-generated method for 'listLprEvents'

    Fetches license plate recognition events. Filters can be applied to search for specific events based on
the make and model of the vehicle, the color of the vehicle, the direction of the vehicle, the access
type, the actor, and the user data. For a list of possible values for each field, refer to the
[`/lprEvents:listFieldValues`](ref:listlpreventfieldvalues) endpoint.

The `include` parameter can be used to specify which data schemas should be included in the response. If no
`include` parameter is provided, the response will include only the base event envelope.

    HTTP Method: GET
    Endpoint: /lprEvents

    Parameters:
        - timestamp__gte (query): Provide timestamp to fetch events after this time. Format - 20220626183000.000
        - timestamp__lte (query): Provide timestamp to fetch events before this time. Format - 20220626183000.000
        - plateConfidence__lte (query): Provide the confidence value to fetch events with confidence less than or equal to the provided value.
        - plate (query): Provide the license plate in uppercase to be searched with an exact match. You can pass `plate`, `plate__fuzzy`, or `plate__contains` as a query parameter, but not more than one. Doing so will result in a `400 Bad Request` error
        - plate__fuzzy (query): Provide the license plate for fuzzy search that allows for a single character difference. You can pass `plate`, `plate__fuzzy`, or `plate__contains` as a query parameter, but not more than one. Doing so will result in a `400 Bad Request` error
        - plate__contains (query): Provide the license plate for searching substrings or exact match license plate. Refrain from passing asterisk `*` else will get `400 Bad Request`. You can pass `plate`, `plate__fuzzy`, or `plate__contains` as a query parameter, but not more than one. Doing so will result in a `400 Bad Request` error
        - type__in (query): Filter events based on the type of event
        - recognizedText (query): Provide the text to be searched with an exact match in any of license plate, dot number, truck number, trailer number and recognized text. You can pass only one of `recognizedText`, `recognizedText__fuzzy`, or `recognizedText__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - recognizedText__contains (query): Provide the text for partial search that allows for a searching partial string in any of license plate, dot number, truck number, trailer number and recognized text. You can pass only one of `recognizedText`, `recognizedText__fuzzy`, or `recognizedText__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - recognizedText__fuzzy (query): Provide the text for fuzzy search that allows for a single character difference in any of license plate, dot number, truck number, trailer number and recognized text. You can pass only one of `recognizedText`, `recognizedText__fuzzy`, or `recognizedText__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - direction__in (query): Fetch events based on the direction of vehicle
        - accessType__in (query): Search based on the access type
        - actor (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list. For each entry of list, the actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to filter for camera with id 100d4c41, the actorId that has to be used is `camera:100d4c41`. To search for events from a specific type of actor, for example users, use a wildcard as actorId: `user:*`.

        - color__in (query): Fetch events based on the color of vehicle
        - make__in (query): Fetch events based on make of vehicle. Examples are "ford", "toyota" etc.
        - bodyType__in (query): Fetch events based on body type of vehicle. Examples are "sedan", "jeep" etc.
        - data.een.userData.v1 (query): Dynamically named query parameter that allows clients to filter events based on specific values in user supplied fields.
  * This allows searching by user supplied attributes instead of plates, for example, apartment number, organization etc.
  * If the user for example wishes to search for `organization` having value `ABC` then the correct way to search is `data.een.userData.v1.organization=ABC`. This then needs to be specified directly in the query parameters or in json object as a key value pair.
  * The list of user Data keys can be obtained by calling `/lprVehicleLists:listFields` endpoint
        - data.een.dotNumberRecognition.v1.regNumber (query): Provide the number to be searched with an exact match in the dot number recognition data. You can pass only one of `data.een.dotNumberRecognition.v1.regNumber`, `data.een.dotNumberRecognition.v1.regNumber__fuzzy`, or `data.een.dotNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.dotNumberRecognition.v1.regNumber__contains (query): Provide the number for partial search that allows for a searching partial string in the dot number recognition data. You can pass only one of `data.een.dotNumberRecognition.v1.regNumber`, `data.een.dotNumberRecognition.v1.regNumber__fuzzy`, or `data.een.dotNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.dotNumberRecognition.v1.regNumber__fuzzy (query): Provide the number for fuzzy search that allows for a single character difference in the dot number recognition data. You can pass only one of `data.een.dotNumberRecognition.v1.regNumber`, `data.een.dotNumberRecognition.v1.regNumber__fuzzy`, or `data.een.dotNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.truckNumberRecognition.v1.regNumber (query): Provide the number to be searched with an exact match in the truck number recognition data. You can pass only one of `data.een.truckNumberRecognition.v1.regNumber`, `data.een.truckNumberRecognition.v1.regNumber__fuzzy`, or `data.een.truckNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.truckNumberRecognition.v1.regNumber__contains (query): Provide the number for partial search that allows for a searching partial string in the truck number recognition data. You can pass only one of `data.een.truckNumberRecognition.v1.regNumber`, `data.een.truckNumberRecognition.v1.regNumber__fuzzy`, or `data.een.truckNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.truckNumberRecognition.v1.regNumber__fuzzy (query): Provide the number for fuzzy search that allows for a single character difference in the truck number recognition data. You can pass only one of `data.een.truckNumberRecognition.v1.regNumber`, `data.een.truckNumberRecognition.v1.regNumber__fuzzy`, or `data.een.truckNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.trailerNumberRecognition.v1.regNumber (query): Provide the number to be searched with an exact match in the trailer number recognition data. You can pass only one of `data.een.trailerNumberRecognition.v1.regNumber`, `data.een.trailerNumberRecognition.v1.regNumber__fuzzy`, or `data.een.trailerNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.trailerNumberRecognition.v1.regNumber__contains (query): Provide the number for partial search that allows for a searching partial string in the trailer number recognition data. You can pass only one of `data.een.trailerNumberRecognition.v1.regNumber`, `data.een.trailerNumberRecognition.v1.regNumber__fuzzy`, or `data.een.trailerNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.trailerNumberRecognition.v1.regNumber__fuzzy (query): Provide the number for fuzzy search that allows for a single character difference in the trailer number recognition data. You can pass only one of `data.een.trailerNumberRecognition.v1.regNumber`, `data.een.trailerNumberRecognition.v1.regNumber__fuzzy`, or `data.een.trailerNumberRecognition.v1.regNumber__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.lprPlateRead.v1.plate (query): Provide the license plate in uppercase to be searched with an exact match in the lpr plate read data. You can pass only one of `data.een.lprPlateRead.v1.plate`, `data.een.lprPlateRead.v1.plate__fuzzy`, or `data.een.lprPlateRead.v1.plate__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.lprPlateRead.v1.plate__contains (query): Provide the license plate for partial search that allows for a searching partial string in the lpr plate read data. You can pass only one of `data.een.lprPlateRead.v1.plate`, `data.een.lprPlateRead.v1.plate__fuzzy`, or `data.een.lprPlateRead.v1.plate__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.lprPlateRead.v1.plate__fuzzy (query): Provide the license plate for fuzzy search that allows for a single character difference in the lpr plate read data. You can pass only one of `data.een.lprPlateRead.v1.plate`, `data.een.lprPlateRead.v1.plate__fuzzy`, or `data.een.lprPlateRead.v1.plate__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.recognizedText.v1.value (query): Provide the recognized text value to be searched with an exact match in the recognized text detection data. You can pass only one of `data.een.recognizedText.v1.value`, `data.een.recognizedText.v1.value__fuzzy`, or `data.een.recognizedText.v1.value__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.recognizedText.v1.value__contains (query): Provide the recognized text value for partial search that allows for a searching partial string in the recognized text detection data. You can pass only one of `data.een.recognizedText.v1.value`, `data.een.recognizedText.v1.value__fuzzy`, or `data.een.recognizedText.v1.value__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - data.een.recognizedText.v1.value__fuzzy (query): Provide the recognized text value for fuzzy search that allows for a single character difference in the recognized text detection data. You can pass only one of `data.een.recognizedText.v1.value`, `data.een.recognizedText.v1.value__fuzzy`, or `data.een.recognizedText.v1.value__contains` as a query parameter. Passing multiple will cause a `400 Bad Request` error.
        - searchRelatedEventData (query): If set to true, the API will search for related events based on the license plate, dot number, truck number, trailer number and recognized text. This will return all events that are related to the search criteria.
        - relatedEvents.rel (query): Used to Filter relatedEvents based on the relationship type.
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - include (query): Provide fields to be returned in response body

    Responses:
        - 200: List of events matching search criteria
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/lprEvents"
    params = {}
    if timestamp__gte is not None:
        params['timestamp__gte'] = timestamp__gte
    if timestamp__lte is not None:
        params['timestamp__lte'] = timestamp__lte
    if plateConfidence__lte is not None:
        params['plateConfidence__lte'] = plateConfidence__lte
    if plate is not None:
        params['plate'] = plate
    if plate__fuzzy is not None:
        params['plate__fuzzy'] = plate__fuzzy
    if plate__contains is not None:
        params['plate__contains'] = plate__contains
    if type__in is not None:
        if isinstance(type__in, list):
            params['type__in'] = ','.join(map(str, type__in))
        else:
            params['type__in'] = str(type__in)
    if recognizedText is not None:
        params['recognizedText'] = recognizedText
    if recognizedText__contains is not None:
        params['recognizedText__contains'] = recognizedText__contains
    if recognizedText__fuzzy is not None:
        params['recognizedText__fuzzy'] = recognizedText__fuzzy
    if direction__in is not None:
        if isinstance(direction__in, list):
            params['direction__in'] = ','.join(map(str, direction__in))
        else:
            params['direction__in'] = str(direction__in)
    if accessType__in is not None:
        if isinstance(accessType__in, list):
            params['accessType__in'] = ','.join(map(str, accessType__in))
        else:
            params['accessType__in'] = str(accessType__in)
    if actor is not None:
        if isinstance(actor, list):
            params['actor'] = ','.join(map(str, actor))
        else:
            params['actor'] = str(actor)
    if color__in is not None:
        if isinstance(color__in, list):
            params['color__in'] = ','.join(map(str, color__in))
        else:
            params['color__in'] = str(color__in)
    if make__in is not None:
        if isinstance(make__in, list):
            params['make__in'] = ','.join(map(str, make__in))
        else:
            params['make__in'] = str(make__in)
    if bodyType__in is not None:
        params['bodyType__in'] = bodyType__in
    if data_een_userData_v1 is not None:
        params['data_een_userData_v1'] = data_een_userData_v1
    if data_een_dotNumberRecognition_v1_regNumber is not None:
        params['data_een_dotNumberRecognition_v1_regNumber'] = data_een_dotNumberRecognition_v1_regNumber
    if data_een_dotNumberRecognition_v1_regNumber__contains is not None:
        params['data_een_dotNumberRecognition_v1_regNumber__contains'] = data_een_dotNumberRecognition_v1_regNumber__contains
    if data_een_dotNumberRecognition_v1_regNumber__fuzzy is not None:
        params['data_een_dotNumberRecognition_v1_regNumber__fuzzy'] = data_een_dotNumberRecognition_v1_regNumber__fuzzy
    if data_een_truckNumberRecognition_v1_regNumber is not None:
        params['data_een_truckNumberRecognition_v1_regNumber'] = data_een_truckNumberRecognition_v1_regNumber
    if data_een_truckNumberRecognition_v1_regNumber__contains is not None:
        params['data_een_truckNumberRecognition_v1_regNumber__contains'] = data_een_truckNumberRecognition_v1_regNumber__contains
    if data_een_truckNumberRecognition_v1_regNumber__fuzzy is not None:
        params['data_een_truckNumberRecognition_v1_regNumber__fuzzy'] = data_een_truckNumberRecognition_v1_regNumber__fuzzy
    if data_een_trailerNumberRecognition_v1_regNumber is not None:
        params['data_een_trailerNumberRecognition_v1_regNumber'] = data_een_trailerNumberRecognition_v1_regNumber
    if data_een_trailerNumberRecognition_v1_regNumber__contains is not None:
        params['data_een_trailerNumberRecognition_v1_regNumber__contains'] = data_een_trailerNumberRecognition_v1_regNumber__contains
    if data_een_trailerNumberRecognition_v1_regNumber__fuzzy is not None:
        params['data_een_trailerNumberRecognition_v1_regNumber__fuzzy'] = data_een_trailerNumberRecognition_v1_regNumber__fuzzy
    if data_een_lprPlateRead_v1_plate is not None:
        params['data_een_lprPlateRead_v1_plate'] = data_een_lprPlateRead_v1_plate
    if data_een_lprPlateRead_v1_plate__contains is not None:
        params['data_een_lprPlateRead_v1_plate__contains'] = data_een_lprPlateRead_v1_plate__contains
    if data_een_lprPlateRead_v1_plate__fuzzy is not None:
        params['data_een_lprPlateRead_v1_plate__fuzzy'] = data_een_lprPlateRead_v1_plate__fuzzy
    if data_een_recognizedText_v1_value is not None:
        params['data_een_recognizedText_v1_value'] = data_een_recognizedText_v1_value
    if data_een_recognizedText_v1_value__contains is not None:
        params['data_een_recognizedText_v1_value__contains'] = data_een_recognizedText_v1_value__contains
    if data_een_recognizedText_v1_value__fuzzy is not None:
        params['data_een_recognizedText_v1_value__fuzzy'] = data_een_recognizedText_v1_value__fuzzy
    if searchRelatedEventData is not None:
        params['searchRelatedEventData'] = searchRelatedEventData
    if relatedEvents_rel is not None:
        params['relatedEvents_rel'] = relatedEvents_rel
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
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


def get_lpr_event(self, id, include=None):
    """Auto-generated method for 'getLprEvent'

    Fetches lpr event based on `id` provided. This returns the event as an extension of event base envelope with LPR specific information

    HTTP Method: GET
    Endpoint: /lprEvents/{id}

    Parameters:
        - id (path): Id
        - include (query): Provide fields to be returned in response body

    Responses:
        - 200: Event details
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprEvents/{id}"
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


def get_lpr_events_summary(self, userTime=None, include=None, groupBy=None, plateConfidence__lte=None, type__in=None):
    """Auto-generated method for 'getLprEventsSummary'

    Fetches summary of lpr event counts. Query fields can control the parameters that are returned in the response body. There are 7 key attributes as follows:
  * `lastHour` : event count in last one hour.
  * `last24h` : event count in last 24 hours.
  * `today`: event count in current day from 00:00 user local time to present
  * `yesterday` : events for previous day (in user's local time zone)
  * `last7Days` : event count in last 7 days.
  * `last30Days` : event count in last 30 days
  * `latestEventTimestamp` : timestamp of the latest event.

  
At least one of these attributes must be specified for the query to return results. The attributes given apply on each camera and to a single aggregated total.


    HTTP Method: GET
    Endpoint: /lprEvents:summary

    Parameters:
        - userTime (query): The caller can also send the userTime along with timezone to the API. This will be used to calculate the current_day count (as per user local time from 00:00 midnight). Time in ISO-8601 format
        - include (query): Provide fields to be returned in response body
        - groupBy (query): If defined with `actorId` as value, the values are grouped per actor. If not defined, the counts will be aggregated to a single value for all actors.
        - plateConfidence__lte (query): Provide the confidence value to fetch events with confidence less than or equal to the provided value.
        - unknown (None): No description provided
        - type__in (query): Filter events based on the type of event

    Responses:
        - 200: Events summary as requested
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/lprEvents:summary"
    params = {}
    if userTime is not None:
        params['userTime'] = userTime
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if groupBy is not None:
        params['groupBy'] = groupBy
    if plateConfidence__lte is not None:
        params['plateConfidence__lte'] = plateConfidence__lte
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


def list_lpr_event_field_values(self):
    """Auto-generated method for 'listLprEventFieldValues'

    Fetches all of the possible values for each of the fields that can be used to filter LPR events.

    HTTP Method: GET
    Endpoint: /lprEvents:listFieldValues

    Responses:
        - 200: Success, lists field values as populated in the events.
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/lprEvents:listFieldValues"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
