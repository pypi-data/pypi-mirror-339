def get_media_session(self):
    """Auto-generated method for 'getMediaSession'

    Api to list the url to call to set the media session cookie. The call will also redirect to the same url.
The media session cookie can be used to replace the bearer authentication for mp4 playback in web browsers.


    HTTP Method: GET
    Endpoint: /media/session

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
        - 503: The service or resource is currently not available
    """
    endpoint = "/media/session"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
