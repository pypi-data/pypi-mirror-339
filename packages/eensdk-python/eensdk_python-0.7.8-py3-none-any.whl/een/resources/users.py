def get_users(self, include=None, sort=None, pageToken=None, pageSize=None, id__in=None, id__notIn=None, locationId__in=None, locationId__ne=None, firstName__in=None, firstName__contains=None, lastName__in=None, lastName__contains=None, email__in=None, email__contains=None, permissions_administrator=None, status_loginStatus__in=None, q=None, qRelevance__gte=None):
    """Auto-generated method for 'getUsers'

    This endpoint allows the users to retrieve a list of users within the account. This endpoint supports filtering, pagination, and sorting, as well as including additional information with the response.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available users, not the number of users resulting from the query string.


    HTTP Method: GET
    Endpoint: /users

    Parameters:
        - include (query): No description provided
        - sort (query): Comma separated list of of fields that should be sorted. By default, the users response is sorted by first name.
 * `sort=` - not providing any value will result in error 400
 * `sort=+firstName,+firstName` - same values will result in error 400
 * `sort=-firstName,+firstName` - mutually exclusive values will return error 400
 * maxItem=5 - Only five values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400

        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - id__in (query): Filter to get the users whose id is on the provided list. The lookup is exact and case insensitive.
        - id__notIn (query): Filter to exlude the users whose ids are in the provided list. The lookup is exact and case insensitive.
        - locationId__in (query): List of Location IDs to filter on that is comma separated.
        - locationId__ne (query): Filter to get the users with an locationId that is not equal to the provided value. The lookup is exact but case insensitive.
        - firstName__in (query): Filter to get the users whose firstName is on the provided list. The lookup is exact but case insensitive
        - firstName__contains (query): Filter to get the users whose the firstName contains the provided substring. The lookup is exact but case insensitive

        - lastName__in (query): Filter to get the users whose lastName is on the provided list. The lookup is exact but case insensitive
        - lastName__contains (query): Filter to get the users whose the lastName contains the provided substring. The lookup is exact but case insensitive

        - email__in (query): Filter to get the users whose email is on the provided list. The lookup is exact but case insensitive
        - email__contains (query): Filter to get the users whose the email contains provided substring. The lookup is exact but case insensitive

        - permissions.administrator (query): Filter to get the users with provided administrator value.

        - status.loginStatus__in (query): Filter to get the users whose loginStatus is on the provided list. The lookup is exact but case insensitive
        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched: `firstName`, `lastName`, `email`.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).


    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/users"
    params = {}
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
    if sort is not None:
        if isinstance(sort, list):
            params['sort'] = ','.join(map(str, sort))
        else:
            params['sort'] = str(sort)
    if pageToken is not None:
        params['pageToken'] = pageToken
    if pageSize is not None:
        params['pageSize'] = pageSize
    if id__in is not None:
        if isinstance(id__in, list):
            params['id__in'] = ','.join(map(str, id__in))
        else:
            params['id__in'] = str(id__in)
    if id__notIn is not None:
        if isinstance(id__notIn, list):
            params['id__notIn'] = ','.join(map(str, id__notIn))
        else:
            params['id__notIn'] = str(id__notIn)
    if locationId__in is not None:
        if isinstance(locationId__in, list):
            params['locationId__in'] = ','.join(map(str, locationId__in))
        else:
            params['locationId__in'] = str(locationId__in)
    if locationId__ne is not None:
        params['locationId__ne'] = locationId__ne
    if firstName__in is not None:
        if isinstance(firstName__in, list):
            params['firstName__in'] = ','.join(map(str, firstName__in))
        else:
            params['firstName__in'] = str(firstName__in)
    if firstName__contains is not None:
        params['firstName__contains'] = firstName__contains
    if lastName__in is not None:
        if isinstance(lastName__in, list):
            params['lastName__in'] = ','.join(map(str, lastName__in))
        else:
            params['lastName__in'] = str(lastName__in)
    if lastName__contains is not None:
        params['lastName__contains'] = lastName__contains
    if email__in is not None:
        if isinstance(email__in, list):
            params['email__in'] = ','.join(map(str, email__in))
        else:
            params['email__in'] = str(email__in)
    if email__contains is not None:
        params['email__contains'] = email__contains
    if permissions_administrator is not None:
        params['permissions_administrator'] = permissions_administrator
    if status_loginStatus__in is not None:
        if isinstance(status_loginStatus__in, list):
            params['status_loginStatus__in'] = ','.join(map(str, status_loginStatus__in))
        else:
            params['status_loginStatus__in'] = str(status_loginStatus__in)
    if q is not None:
        params['q'] = q
    if qRelevance__gte is not None:
        params['qRelevance__gte'] = qRelevance__gte
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_user(self, body):
    """Auto-generated method for 'createUser'

    This endpoint allows users to create a user in the account. The created user will be in pending state and a verification email will be sent to the user. Once approved, the newly created user will be in active state and will be able to be used.


    HTTP Method: POST
    Endpoint: /users

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - firstName (string): First name of the user.

        - lastName (string): Last name of the user.

        - locationId (string): ID Of the location.
        - email (string): This email is used for login.
        - permissions (object): No description provided.
        - roles (array): List of role IDs assigned to the user. When a user is created, they can only have either roles or permissions assigned. Furthermore, the roles feature has to be enabled for the account.

        - grantAllLayouts (boolean): Indicates whether the newly created user will inherit access to all layouts from the user who created them.

        - grantAllCameras (boolean): Indicates whether the newly created user will inherit access to all cameras from the user who created them.

        - grantAllLocations (boolean): Indicates whether the newly created user will inherit access to all locations from the user who created them.

        - grantAllAccounts (boolean): Indicates whether the newly created user will inherit access to all accounts from the user who created them. It should be used only from reseller context. In case of used from the sub-account context the flag will be ignored.


    Responses:
        - 201: User Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = "/users"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_user(self, userId, include=None):
    """Auto-generated method for 'getUser'

    This endpoint allows the users to retrieve info about a specific user based on the user ID.

    HTTP Method: GET
    Endpoint: /users/{userId}

    Parameters:
        - userId (path): No description provided
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/users/{userId}"
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


def delete_user(self, userId):
    """Auto-generated method for 'deleteUser'

    This endpoint allows the users to delete a user from the account, removing all references related to that user.


    HTTP Method: DELETE
    Endpoint: /users/{userId}

    Parameters:
        - userId (path): No description provided

    Responses:
        - 204: User deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/users/{userId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def update_user(self, body, userId):
    """Auto-generated method for 'updateUser'

    This endpoint allows the users to updat a user's data.

    HTTP Method: PATCH
    Endpoint: /users/{userId}

    Parameters:
        - userId (path): No description provided

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - firstName (string): No description provided.
        - lastName (string): No description provided.
        - email (string): This email is used for login.
        - locationId (string): ID Of the location.
        - status (string): User can be enabled if set to "active" and disabled if set to "blocked"
        - loginSchedule (object): It signifies a week long alert schedule. This schedule is effective according to actor's (user/camera/account) timezone. It allows setting different times for different days.

        - permissions (object): No description provided.
        - employeeId (string): Custom text field

    Responses:
        - 204: User Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/users/{userId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def get_current_user(self, include=None):
    """Auto-generated method for 'getCurrentUser'

    This endpoint allows the users to retrieve info about the current user.

    HTTP Method: GET
    Endpoint: /users/self

    Parameters:
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/users/self"
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


def update_current_user(self, body):
    """Auto-generated method for 'updateCurrentUser'

    This endpoint allows the users to update current user's data.

    HTTP Method: PATCH
    Endpoint: /users/self

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - firstName (string): No description provided.
        - lastName (string): No description provided.
        - email (string): This email is used for login.
        - contactDetails (object): No description provided.
        - support (object): No description provided.
        - language (string): No description provided.
        - timeZone (object): No description provided.
        - layoutSettings (object): No description provided.
        - previewSettings (object): No description provided.
        - timeSettings (object): No description provided.

    Responses:
        - 204: User Updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/users/self"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def get_trusted_clients(self, include=None):
    """Auto-generated method for 'getTrustedClients'

    This endpoint allows you to retrieve a list of trusted clients.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available trusted clients, not the number of trusted clients resulting from the query string.


    HTTP Method: GET
    Endpoint: /users/self/trustedClients

    Parameters:
        - include (query): No description provided
        - unknown (None): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 500: No description provided
    """
    endpoint = "/users/self/trustedClients"
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


def delete_trusted_client(self, trustedClientId):
    """Auto-generated method for 'deleteTrustedClient'

    This endpoint allows you to delete a trusted client.


    HTTP Method: DELETE
    Endpoint: /users/self/trustedClients/{trustedClientId}

    Parameters:
        - trustedClientId (path): No description provided

    Responses:
        - 204: Trusted client deleted.
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/users/self/trustedClients/{trustedClientId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
