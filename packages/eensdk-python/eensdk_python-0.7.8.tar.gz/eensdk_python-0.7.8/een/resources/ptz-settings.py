def get_ptz_settings(self, cameraId):
    """Auto-generated method for 'getPtzSettings'

    Retrieves the PTZ settings for the given camera.

    HTTP Method: GET
    Endpoint: /cameras/{cameraId}/ptz/settings

    Parameters:
        - cameraId (path): ID of camera we want to operate on.

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = f"/cameras/{cameraId}/ptz/settings"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_ptz_settings(self, body, cameraId):
    """Auto-generated method for 'updatePtzSettings'

    Updates the PTZ settings for the given camera.

    HTTP Method: PATCH
    Endpoint: /cameras/{cameraId}/ptz/settings

    Parameters:
        - cameraId (path): ID of camera we want to operate on.

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - presets (array): Saved positions. Order of this array will be used by the tour mode.
        - homePreset (string): Name of the default preset to which the camera will return if set to homeReturn after the specified auto start delay.
        - mode (string): The following modes are available:
  * `manualOnly`: The PTZ camera will only move when issued a direct command by the user.
  * `homeReturn`: After a specified amount of time without receiving a command,
the PTZ camera will navigate back to the home preset position.  If none is set, this will be the factory default position.
  * `tour`: After the specified auto start delay, the PTZ camera will tour through all
presets in the order specified by the user. It will continue doing so until interrupted and will resume after the aforementioned auto start delay.

        - autoStartDelay (integer): The time in seconds after which the PTZ camera should resume Touring or return to Home when idling.

    Responses:
        - 204: Camera Updated
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}/ptz/settings"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
