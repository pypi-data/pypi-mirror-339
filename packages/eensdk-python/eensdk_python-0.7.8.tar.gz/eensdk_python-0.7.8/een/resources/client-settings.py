def get_client_settings(self):
    """Auto-generated method for 'getClientSettings'

    Retrieves settings required to let the client successfully use the API.

    HTTP Method: GET
    Endpoint: /clientSettings

    Responses:
        - 200: OK
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/clientSettings"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
