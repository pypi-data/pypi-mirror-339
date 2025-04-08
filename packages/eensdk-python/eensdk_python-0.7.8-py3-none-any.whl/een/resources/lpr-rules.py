def add_lpr_alert_condition_rule(self, body):
    """Auto-generated method for 'addLprAlertConditionRule'

    Create a new rule that produces alerts based on certain conditions. Specifically, the user specifies alert conditions that indicate when the alert is produced based on following:
  * Which resources (cameras, account or location) can produce the alert
  * What is the schedule for the alert.
  * What event types, or which vehicles (specific plates, or belonging to a vehicleList) can produce the alert.

    HTTP Method: POST
    Endpoint: /lprAlertConditionRules

    Request Body:
        - body (application/json):
            Description: Data containing information on the rule to be added
            Required: True

    Responses:
        - 201: Response on successful creation of requested lpr alertConditionRule
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/lprAlertConditionRules"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def list_lpr_alert_condition_rules(self, actor=None, name__contains=None, type__in=None, priority__lte=None, priority__gte=None, enabled=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'listLprAlertConditionRules'

    Fetches lpr rules based on a filter

    HTTP Method: GET
    Endpoint: /lprAlertConditionRules

    Parameters:
        - actor (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list. For each entry of list, the actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to filter for camera with id 100d4c41, the actorId that has to be used is `camera:100d4c41`. To search for events from a specific type of actor, for example users, use a wildcard as actorId: `user:*`.

        - name__contains (query): Phrase that is used to search for resources (rules or lists) whose names contain it
        - type__in (query): Search based on the rule type
        - priority__lte (query): Filter by priority__lte
        - priority__gte (query): Filter by priority__gte
        - enabled (query): Filter against enabled rules (when set to true) or disabled rules (when set to false)
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: All the rules that met the filter criteria of this API inputs.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: Referenced resource could not be found.
        - 500: No description provided
    """
    endpoint = "/lprAlertConditionRules"
    params = {}
    if actor is not None:
        if isinstance(actor, list):
            params['actor'] = ','.join(map(str, actor))
        else:
            params['actor'] = str(actor)
    if name__contains is not None:
        params['name__contains'] = name__contains
    if type__in is not None:
        params['type__in'] = type__in
    if priority__lte is not None:
        params['priority__lte'] = priority__lte
    if priority__gte is not None:
        params['priority__gte'] = priority__gte
    if enabled is not None:
        params['enabled'] = enabled
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


def get_lpr_alert_condition_rule_field_values(self):
    """Auto-generated method for 'getLprAlertConditionRuleFieldValues'

    Fetches the list of field values across all the attributes of alertConditionRules stored for this account.

    HTTP Method: GET
    Endpoint: /lprAlertConditionRules:listFieldValues

    Responses:
        - 200: Success, returns possible values of each field
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/lprAlertConditionRules:listFieldValues"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_lpr_alert_condition_rule(self, id):
    """Auto-generated method for 'getLprAlertConditionRule'

    Get details of a specific rule id

    HTTP Method: GET
    Endpoint: /lprAlertConditionRules/{id}

    Parameters:
        - id (path): Id

    Responses:
        - 200: Success, returns the rule details
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprAlertConditionRules/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_lpr_alert_condition_rule(self, body, id):
    """Auto-generated method for 'updateLprAlertConditionRule'

    Updates the properties of a specific rule. Only the user defined fields can be updated by this method.

    HTTP Method: PATCH
    Endpoint: /lprAlertConditionRules/{id}

    Parameters:
        - id (path): Id

    Request Body:
        - body (application/json):
            Description: Data containing information on the rule to be added
            Required: True

    Responses:
        - 204: Updated the rule
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprAlertConditionRules/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_lpr_alert_condition_rule(self, id):
    """Auto-generated method for 'deleteLprAlertConditionRule'

    Deletes the rule corresponding to the rule ID

    HTTP Method: DELETE
    Endpoint: /lprAlertConditionRules/{id}

    Parameters:
        - id (path): Id

    Responses:
        - 204: Deleted the rule
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprAlertConditionRules/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
