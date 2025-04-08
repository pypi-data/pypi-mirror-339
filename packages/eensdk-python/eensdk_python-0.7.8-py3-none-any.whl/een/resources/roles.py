def get_roles(self, roleName__contains=None, include=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'getRoles'

    This endpoint returns a list of all roles in current user's account.


    HTTP Method: GET
    Endpoint: /roles

    Parameters:
        - roleName__contains (query): Filter to get the user role assignments whose the role name contains the provided substring. The lookup is exact but case insensitive

        - include (query): No description provided
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: List of roles.
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/roles"
    params = {}
    if roleName__contains is not None:
        params['roleName__contains'] = roleName__contains
    if include is not None:
        if isinstance(include, list):
            params['include'] = ','.join(map(str, include))
        else:
            params['include'] = str(include)
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


def create_role(self, body):
    """Auto-generated method for 'createRole'

    This endpoint creates a new role under the current user's account. Admins can create roles and define which permissions are part of which roles. Non-admin users with 'Role' permission can only create a role with the permission that they already have themselves.


    HTTP Method: POST
    Endpoint: /roles

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): The name of the role.
        - notes (string): The notes of the role.
        - default (boolean): True if the role is one of the default roles for the account, false otherwise.
        - permissions (object): No description provided.

    Responses:
        - 201: Role created.
        - 400: No description provided
        - 401: No description provided
        - 403: You have no permission to access the specified resource.
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = "/roles"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def delete_role(self, roleId):
    """Auto-generated method for 'deleteRole'

    This endpoint deletes a role from current user's account. A role can only be deleted if it is not assigned to any user. Admin users and non-admin users with 'Role' permission can delete roles.


    HTTP Method: DELETE
    Endpoint: /roles/{roleId}

    Parameters:
        - roleId (path): The ID of the role.

    Responses:
        - 204: Role deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: Referenced resource could not be found.
        - 409: No description provided
        - 500: No description provided
    """
    endpoint = f"/roles/{roleId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_role(self, roleId, include=None):
    """Auto-generated method for 'getRole'

    This endpoint returns a role by its ID.


    HTTP Method: GET
    Endpoint: /roles/{roleId}

    Parameters:
        - roleId (path): The ID of the role.
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: No description provided
        - 401: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/roles/{roleId}"
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


def update_role(self, body, roleId):
    """Auto-generated method for 'updateRole'

    This endpoint updates a role. Admin users and non-admin users with 'Role' permission can update roles.


    HTTP Method: PATCH
    Endpoint: /roles/{roleId}

    Parameters:
        - roleId (path): The ID of the role.

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - name (string): The name of the role.
        - notes (string): The notes of the role.
        - default (boolean): True if the role is one of the default roles for the account, false otherwise.
        - permissions (object): No description provided.

    Responses:
        - 204: Role updated.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: No description provided
        - 500: No description provided
    """
    endpoint = f"/roles/{roleId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def get_role_assignments(self, userId__in=None, roleId__in=None, roleId__contains=None, self_=None):
    """Auto-generated method for 'getRoleAssignments'

    This endpoint returns a list of all role assignments in current user's account.

    HTTP Method: GET
    Endpoint: /roleAssignments

    Parameters:
        - userId__in (query): List of user IDs to filter on that is comma separated.
        - roleId__in (query): List of role IDs to filter on that is comma separated.
        - roleId__contains (query): Filter to get the user role assignments whose the role ID contains the provided substring. The lookup is exact but case insensitive

        - unknown (None): No description provided
        - self (query): Filter to get the role assignments for the requesting user.

    Responses:
        - 200: List of role assignments.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/roleAssignments"
    params = {}
    if userId__in is not None:
        if isinstance(userId__in, list):
            params['userId__in'] = ','.join(map(str, userId__in))
        else:
            params['userId__in'] = str(userId__in)
    if roleId__in is not None:
        if isinstance(roleId__in, list):
            params['roleId__in'] = ','.join(map(str, roleId__in))
        else:
            params['roleId__in'] = str(roleId__in)
    if roleId__contains is not None:
        params['roleId__contains'] = roleId__contains
    if self_ is not None:
        params['self_'] = self_
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def create_role_assignments(self, body):
    """Auto-generated method for 'createRoleAssignments'

    This endpoint allows you to create multiple role assignments in one request.


    HTTP Method: POST
    Endpoint: /roleAssignments:bulkcreate

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 200: Operations performed successfully
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/roleAssignments:bulkcreate"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def delete_role_assignments(self, body):
    """Auto-generated method for 'deleteRoleAssignments'

    This endpoint allows you to delete multiple role assignments in one request.


    HTTP Method: POST
    Endpoint: /roleAssignments:bulkdelete

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 200: Operations performed successfully
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/roleAssignments:bulkdelete"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
