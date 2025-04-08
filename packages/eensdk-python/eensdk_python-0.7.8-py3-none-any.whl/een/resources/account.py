def list_accounts(self, include=None):
    """Auto-generated method for 'listAccounts'

    Retrieves a list of accounts the user has access to. This will include the user's own account, but can contain others such as when the user is a reseller.

    HTTP Method: GET
    Endpoint: /accounts

    Parameters:
        - include (query): No description provided

    Responses:
        - 200: OK
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/accounts"
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


def delete_credential(self, credentialId, id):
    """Auto-generated method for 'deleteCredential'

    Deletes the credential from the account.


    HTTP Method: DELETE
    Endpoint: /accounts/{id}/credentials/{credentialId}

    Parameters:
        - credentialId (path): Credential ID
        - id (path): Account ID.  Use __*self*__ as the Account ID to reference the account of the current session


    Responses:
        - 204: Credential deleted.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/accounts/{id}/credentials/{credentialId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
