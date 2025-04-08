def list_speakers(self, include=None, sort=None, pageToken=None, pageSize=None, locationId__in=None, bridgeId__in=None, tags__contains=None, tags__any=None, name__contains=None, name__in=None, name=None, id__in=None, id__contains=None, q=None, qRelevance__gte=None):
    """Auto-generated method for 'listSpeakers'

    Retrieving a list of speakers is possible with this endpoint.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available speakers,  not the number of speakers resulting from the query string.


    HTTP Method: GET
    Endpoint: /speakers

    Parameters:
        - include (query): No description provided
        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=2 - Only two values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400

        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - locationId__in (query): List of Location IDs to filter on that is comma separated.
        - bridgeId__in (query): List of Bridge IDs to filter on that is comma separated.
        - tags__contains (query): Only return speakers that have all tags in the list, separated by commas.
        - tags__any (query): Only return speakers that have one or more of the tags in the list, separated by commas.
        - name__contains (query): Filter to get the speakers whose the name contains the provided substring. The lookup is exact and case insensitive

        - name__in (query): Filter to get the speakers whose name is on the provided list. The lookup is exact and case insensitive.
        - name (query): Filter to get the speakers with the specified name. The lookup is exact and case insensitive.
        - id__in (query): Filter to get the speakers whose id is on the provided list. The lookup is exact and case insensitive.
        - id__contains (query): Filter to get the speakers whose the id contains the provided substring. The lookup is exact and case insensitive

        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched: `id`, `accountId`, `name`, `bridgeId`, `locationId`, `notes`, `tags`, `locationSummary.name`.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/speakers"
    params = {}
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
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if locationId__in is not None:
        if isinstance(locationId__in, list):
            params['locationId__in'] = ','.join(map(str, locationId__in))
        else:
            params['locationId__in'] = str(locationId__in)
    if bridgeId__in is not None:
        params['bridgeId__in'] = bridgeId__in
    if tags__contains is not None:
        if isinstance(tags__contains, list):
            params['tags__contains'] = ','.join(map(str, tags__contains))
        else:
            params['tags__contains'] = str(tags__contains)
    if tags__any is not None:
        if isinstance(tags__any, list):
            params['tags__any'] = ','.join(map(str, tags__any))
        else:
            params['tags__any'] = str(tags__any)
    if name__contains is not None:
        params['name__contains'] = name__contains
    if name__in is not None:
        if isinstance(name__in, list):
            params['name__in'] = ','.join(map(str, name__in))
        else:
            params['name__in'] = str(name__in)
    if name is not None:
        params['name'] = name
    if id__in is not None:
        if isinstance(id__in, list):
            params['id__in'] = ','.join(map(str, id__in))
        else:
            params['id__in'] = str(id__in)
    if id__contains is not None:
        params['id__contains'] = id__contains
    if q is not None:
        params['q'] = q
    if qRelevance__gte is not None:
        params['qRelevance__gte'] = qRelevance__gte
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def add_speaker(self, body=None):
    """Auto-generated method for 'addSpeaker'

    By using this endpoint you can create a speaker.

    HTTP Method: POST
    Endpoint: /speakers

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - mainCredentials (object): The credentials that will used for communicating with the devices with the main API of the device, which generally is its ONVIF API.

        - adminCredentials (object): Credentials that can be shared with end users to allow them to access the camera  API through the tunnel functionality to allow them to manually apply certain advanced configurations. 

        - sipCredentials (object): The credentials that will be used to authenticate SIP sessions.

        - sipPort (integer): Port to which SIP requests should be sent from the bridge. Applicable for sip speakers and defaults to 5060
        - registrationStrategy (string): Indicates how the speaker was added to the system
        - name (string): User-defined name for the device.
        - tags (array): No description provided.
        - bridgeId (string): No description provided.
        - guid (string): No description provided.
        - locationId (string): ID Of the location.

    Responses:
        - 201: Speaker added
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = "/speakers"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_speaker(self, speakerId, include=None):
    """Auto-generated method for 'getSpeaker'

    This endpoint allows you to retrieve a specific speaker.

    HTTP Method: GET
    Endpoint: /speakers/{speakerId}

    Parameters:
        - speakerId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/speakers/{speakerId}"
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


def update_speaker(self, speakerId, body=None):
    """Auto-generated method for 'updateSpeaker'

    This endpoint allows you to update a specific speaker.

    HTTP Method: PATCH
    Endpoint: /speakers/{speakerId}

    Parameters:
        - speakerId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - name (string): User-defined name for the device.
        - notes (string): No description provided.
        - tags (array): No description provided.
        - locationId (string): ID Of the location.

    Responses:
        - 204: Speaker updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/speakers/{speakerId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_speaker(self, speakerId):
    """Auto-generated method for 'deleteSpeaker'

    This endpoint allows you to dis-associate a speaker from the account, removing all references, recordings, and events.  
 
This request will be blocked until the speaker has been fully removed.


    HTTP Method: DELETE
    Endpoint: /speakers/{speakerId}

    Parameters:
        - speakerId (path): No description provided

    Responses:
        - 204: Speaker deleted.
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/speakers/{speakerId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
