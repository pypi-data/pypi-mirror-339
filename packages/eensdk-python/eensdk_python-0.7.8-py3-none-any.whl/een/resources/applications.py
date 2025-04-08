def list_applications(self, pageToken=None, pageSize=None):
    """Auto-generated method for 'listApplications'

    This endpoint allows retrieval of all applications accessible by the requesting user.  
It is important to note that after using the pageSize parameter, the "totalSize" in the  response represents the total number of available applications, not the number of applications resulting from the query string.


    HTTP Method: GET
    Endpoint: /applications

    Parameters:
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/applications"
    params = {}
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_application(self, body):
    """Auto-generated method for 'createApplication'

    This endpoint allows you to create a new application under the requesting user's account. A maximum of 100 applications can be created under the account.


    HTTP Method: POST
    Endpoint: /applications

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the application.
        - displayName (string): Display name of the application.
        - website (string): URL to the website of this application.
        - developer (string): Name of the developer/company which developed this application.
        - privacyPolicy (string): URL to the privacy policy of this application.
        - termsOfService (string): URL to the terms of service of this application.
        - description (string): The description of the application.
        - isPublic (boolean): Whether this application is intended to be public (available for other parties through an application store).
        - logo (string): URL to the logo of the application.
        - technicalContact (object): Request body for application update.

    Responses:
        - 201: Application Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/applications"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_application(self, applicationId):
    """Auto-generated method for 'getApplication'

    This endpoint allows you to retrieve a single application.

    HTTP Method: GET
    Endpoint: /applications/{applicationId}

    Parameters:
        - applicationId (path): Identifier of an application

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_application(self, body, applicationId):
    """Auto-generated method for 'updateApplication'

    This endpoint allows you to update a single application.

    HTTP Method: PATCH
    Endpoint: /applications/{applicationId}

    Parameters:
        - applicationId (path): Identifier of an application

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the application.
        - displayName (string): Display name of the application.
        - website (string): URL to the website of this application.
        - developer (string): Name of the developer/company which developed this application.
        - privacyPolicy (string): URL to the privacy policy of this application.
        - termsOfService (string): URL to the terms of service of this application.
        - description (string): The description of the application.
        - isPublic (boolean): Whether this application is intended to be public (available for other parties through an application store).
        - logo (string): URL to the logo of the application.
        - technicalContact (object): Request body for application update.

    Responses:
        - 204: Application Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_application(self, applicationId):
    """Auto-generated method for 'deleteApplication'

    This endpoint allows you to delete a single application.

    HTTP Method: DELETE
    Endpoint: /applications/{applicationId}

    Parameters:
        - applicationId (path): Identifier of an application

    Responses:
        - 204: Application deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_oauth_clients(self, applicationId):
    """Auto-generated method for 'getOauthClients'

    This endpoint allows retrieval of all OAuth credentials for the given application.  
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available OAuth credentials, not the number of OAuth credentials resulting from the query string.


    HTTP Method: GET
    Endpoint: /applications/{applicationId}/oauthClients

    Parameters:
        - applicationId (path): Identifier of an application
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: Requested content type for response not supported.
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def add_oauth_client(self, body, applicationId):
    """Auto-generated method for 'addOauthClient'

    This endpoint allows you to create a new OAuth client for the given application. A maximum of 250 oauth client credentials can be created under the application.


    HTTP Method: POST
    Endpoint: /applications/{applicationId}/oauthClients

    Parameters:
        - applicationId (path): Identifier of an application

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the oauth client.
        - redirectUris (array): No description provided.
        - loginUris (array): No description provided.
        - type (string): This defines the type of this client . Clients are CONFIDENTIAL by default.

    Responses:
        - 201: Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 415: Content type of request body not supported.
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_oauth_client(self, applicationId, clientId):
    """Auto-generated method for 'getOauthClient'

    This endpoint allows you to retrieve a specific OAuth client.

    HTTP Method: GET
    Endpoint: /applications/{applicationId}/oauthClients/{clientId}

    Parameters:
        - applicationId (path): Identifier of an application
        - clientId (path): Identifier of a OAuth client

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients/{clientId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_client(self, body, applicationId, clientId):
    """Auto-generated method for 'updateClient'

    This endpoint allows you to update a specific Oauth client.

    HTTP Method: PATCH
    Endpoint: /applications/{applicationId}/oauthClients/{clientId}

    Parameters:
        - applicationId (path): Identifier of an application
        - clientId (path): Identifier of a OAuth client

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): Name of the oauth client.
        - redirectUris (array): No description provided.
        - loginUris (array): No description provided.

    Responses:
        - 204: Client Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients/{clientId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_oauth_client(self, applicationId, clientId):
    """Auto-generated method for 'deleteOauthClient'

    This endpoint allows you to delete a specific OAuth client of a given application.

    HTTP Method: DELETE
    Endpoint: /applications/{applicationId}/oauthClients/{clientId}

    Parameters:
        - applicationId (path): Identifier of an application
        - clientId (path): Identifier of a OAuth client

    Responses:
        - 204: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 406: No description provided
        - 500: No description provided
    """
    endpoint = f"/applications/{applicationId}/oauthClients/{clientId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
