def get_speaker_settings(self, speakerId, include=None):
    """Auto-generated method for 'getSpeakerSettings'

    Retrieves the current settings for the given speaker. 


    HTTP Method: GET
    Endpoint: /speakers/{speakerId}/settings

    Parameters:
        - speakerId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = f"/speakers/{speakerId}/settings"
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


def update_speaker_settings(self, body, speakerId):
    """Auto-generated method for 'updateSpeakerSettings'

    Updates the settings of a speaker.


    HTTP Method: PATCH
    Endpoint: /speakers/{speakerId}/settings

    Parameters:
        - speakerId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - data (object): No description provided.
        - schema (object): Json schema of version draft 4.

    Responses:
        - 204: Speaker Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/speakers/{speakerId}/settings"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
