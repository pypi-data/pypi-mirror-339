def get_camera_settings(self, cameraId, include=None):
    """Auto-generated method for 'getCameraSettings'

    Retrieves the current settings for the given camera. 

Since cameras, the bridge they are connected to and the accounts they are part of can have different 
capabilities, not all settings given in this specification will be applicable to all cameras. 
If a setting is applicable, it will be returned by the API, if not, the field(s) will be skipped.


    HTTP Method: GET
    Endpoint: /cameras/{cameraId}/settings

    Parameters:
        - cameraId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = f"/cameras/{cameraId}/settings"
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


def update_camera_settings(self, body, cameraId):
    """Auto-generated method for 'updateCameraSettings'

    Updates the settings of a camera.

It will throw an error if the setting in the payload is not supported by a camera type. 
It won't apply any settings in case of error.


    HTTP Method: PATCH
    Endpoint: /cameras/{cameraId}/settings

    Parameters:
        - cameraId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - data (object): No description provided.
        - schema (object): Json schema of version draft 4.
        - proposedValues (object): Lists of proposed values to be displayed to users for each property. Although users can choose any number of days, this subset keeps the list manageable and agrees with any billing thresholds.

    Responses:
        - 204: Camera Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}/settings"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
