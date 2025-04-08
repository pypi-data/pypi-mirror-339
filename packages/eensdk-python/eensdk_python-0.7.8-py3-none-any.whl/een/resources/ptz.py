def get_current_position(self, cameraId):
    """Auto-generated method for 'getCurrentPosition'

    This endpoint returns the current position of the camera. The response includes the pan, tilt, and zoom values of the camera. If the camera does not support pan or  tilt or zoom, the corresponding value will not be present in the response.


    HTTP Method: GET
    Endpoint: /cameras/{cameraId}/ptz/position

    Parameters:
        - cameraId (path): ID of camera we want to operate on.

    Responses:
        - 200: Current PTZ position of camera.
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = f"/cameras/{cameraId}/ptz/position"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def move_to(self, body, cameraId):
    """Auto-generated method for 'moveTo'

    This endpoint moves the camera to a specific position, in a specific direction, or to a specific center point on the screen. The endpoint accepts a move object that can be either a position move, a direction move or a center move.


    HTTP Method: PUT
    Endpoint: /cameras/{cameraId}/ptz/position

    Parameters:
        - cameraId (path): ID of camera we want to operate on.

    Request Body:
        - body (application/json):
            Description: Describes where to move the camera to, this could be either a directional, center or position move object. For a position move it is possible to only specify the zoom or the pan and tilt you want to move. It is of course also possible to give all 3 coordinates.

            Required: True

    Top-level Request Body Properties:
        - moveType (string): No description provided.

    Responses:
        - 204: Camera moved to given position.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: No description provided
        - 500: No description provided
    """
    endpoint = f"/cameras/{cameraId}/ptz/position"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PUT',
        params=params,
        data=data,
    )
