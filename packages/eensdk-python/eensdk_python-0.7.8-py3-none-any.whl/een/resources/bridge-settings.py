def get_bridge_settings(self, id):
    """Auto-generated method for 'getBridgeSettings'

    Get all the configurable operational settings related to
a bridge

    HTTP Method: GET
    Endpoint: /bridges/{id}/settings/

    Parameters:
        - id (path): No description provided

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = f"/bridges/{id}/settings/"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_bridge_settings(self, body, id):
    """Auto-generated method for 'updateBridgeSettings'

    Updates the settings of a bridge.


    HTTP Method: PATCH
    Endpoint: /bridges/{id}/settings/

    Parameters:
        - id (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - data (object): No description provided.

    Responses:
        - 204: Camera Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/bridges/{id}/settings/"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
