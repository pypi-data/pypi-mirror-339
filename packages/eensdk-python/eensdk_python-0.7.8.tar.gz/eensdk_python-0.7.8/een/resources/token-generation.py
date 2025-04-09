def create_token(self, body):
    """Auto-generated method for 'createToken'

    Resellers can retrieve access tokens for a given end-user account, assuming that the end-user account falls under the reseller's account.


    HTTP Method: POST
    Endpoint: /authorizationTokens

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 201: Token created
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/authorizationTokens"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
