def get_scim_settings(self):
    """Auto-generated method for 'getScimSettings'

    Returns SCIM Settings of the account.


    HTTP Method: GET
    Endpoint: /accounts/self/scimSettings

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/accounts/self/scimSettings"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_scim_settings(self, body):
    """Auto-generated method for 'updateScimSettings'

    Updates SCIM setting of the account.


    HTTP Method: PATCH
    Endpoint: /accounts/self/scimSettings

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - enabled (boolean): True if user management via SCIM is enabled for the account.
        - apiKey (string): You can reset the API key by setting its value to null and null is the only accepted value for this parameter.  Once reset, the previous API key is immediately invalidated with no grace period.

        - managedAssignments (array): List of managed assignments enabled for the account.  When enabling or disabling sites or layouts, both must be enabled or disabled together.


    Responses:
        - 200: SCIM settings updated.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/accounts/self/scimSettings"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )
