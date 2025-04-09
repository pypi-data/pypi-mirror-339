def list_vehicle_lists(self, actor=None, plate=None, name__contains=None, pageToken=None, pageSize=None):
    """Auto-generated method for 'listVehicleLists'

    Fetches the available vehicleLists based on the filter

    HTTP Method: GET
    Endpoint: /lprVehicleLists

    Parameters:
        - actor (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list. For each entry of list, the actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to filter for camera with id 100d4c41, the actorId that has to be used is `camera:100d4c41`. To search for events from a specific type of actor, for example users, use a wildcard as actorId: `user:*`.

        - plate (query): Provide the license plate in uppercase to be searched with an exact match
        - name__contains (query): Phrase that is used to search for resources (rules or lists) whose names contain it
        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.


    Responses:
        - 200: Fetches all the vehicle list that matches the filtering based on the query parameters. Only list properties are returned per list. The individual vehicle records within a list are not returned
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/lprVehicleLists"
    params = {}
    if actor is not None:
        if isinstance(actor, list):
            params['actor'] = ','.join(map(str, actor))
        else:
            params['actor'] = str(actor)
    if plate is not None:
        params['plate'] = plate
    if name__contains is not None:
        params['name__contains'] = name__contains
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


def add_vehicle_list(self, body):
    """Auto-generated method for 'addVehicleList'

    Add a new vehicleList to the user account

    HTTP Method: POST
    Endpoint: /lprVehicleLists

    Request Body:
        - body (application/json):
            Description: Meta configuration for the list
            Required: True

    Top-level Request Body Properties:
        - name (string): User supplied name for the list
        - enabled (boolean): Whether list is enabled
        - notes (string): A verbose explanation of the vehicle list
        - resourceFilter (object): List of actors against which filtering to happen (camera/location/account)

    Responses:
        - 201: Successful creation of the new list
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = "/lprVehicleLists"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_vehicle_list_fields(self):
    """Auto-generated method for 'getVehicleListFields'

    Fetches all available fields in vehicle Lists for this account. Specifically, using this API, the user may:
  * Obtain the list of fields for ordered display of vehicle records, wherein each field is a column.
  * Obtain the possible values for some or all of the fields for search queries.
  * Understand user defined fields in the records of vehicle Lists, which is a dynamic set.

    HTTP Method: GET
    Endpoint: /lprVehicleLists:listFields

    Responses:
        - 200: List of all fields
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/lprVehicleLists:listFields"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_vehicle_list_field_values(self):
    """Auto-generated method for 'getVehicleListFieldValues'

    Fetches the list of field values including possible values for each key in userData.

    HTTP Method: GET
    Endpoint: /lprVehicleLists:listFieldValues

    Responses:
        - 200: Possible values of each field
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = "/lprVehicleLists:listFieldValues"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_vehicle_list(self, id):
    """Auto-generated method for 'getVehicleList'

    Fetches the information about the specific vehicleList but not each vehicle record

    HTTP Method: GET
    Endpoint: /lprVehicleLists/{id}

    Parameters:
        - id (path): Id

    Responses:
        - 200: Returns information about the list. Only list properties are returned and not the individual vehicle records inside it.
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_vehicle_list(self, body, id):
    """Auto-generated method for 'updateVehicleList'

    Update the meta configuration properties about the specific vehicle List

    HTTP Method: PATCH
    Endpoint: /lprVehicleLists/{id}

    Parameters:
        - id (path): Id

    Request Body:
        - body (application/json):
            Description: Configuration properties to be updated
            Required: True

    Top-level Request Body Properties:
        - name (string): User supplied name for the list
        - enabled (boolean): Whether list is enabled
        - notes (string): A verbose explanation of the vehicle list
        - resourceFilter (object): List of actors against which filtering to happen (camera/location/account)

    Responses:
        - 204: Updated the list
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_vehicle_list(self, id):
    """Auto-generated method for 'deleteVehicleList'

    Delete the vehicle list along with the entries

    HTTP Method: DELETE
    Endpoint: /lprVehicleLists/{id}

    Parameters:
        - id (path): Id

    Responses:
        - 204: Deleted the list
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def list_vehicles(self, id, plate=None, accessType__in=None, securityStatus__in=None, userData=None):
    """Auto-generated method for 'listVehicles'

    Fetches information about all the vehicle records in the given list, including the user data.

    HTTP Method: GET
    Endpoint: /lprVehicleLists/{id}/vehicles

    Parameters:
        - id (path): Id
        - unknown (None): No description provided
        - plate (query): Provide the license plate in uppercase to be searched with an exact match
        - accessType__in (query): Search based on the access type
        - securityStatus__in (query): Filters by only those records under a specific type of security status
        - userData (query): Dynamically named query parameter that allows clients to filter events based on specific values in user supplied fields.
  * This allows searching by user supplied attributes instead of plates, for example, apartment number, organization etc.
  * If the user for example wishes to search for `organization` having value `ABC` then the correct way to search is `userData.organization=ABC`. This then needs to be specified directly in the query parameters or in json object as a key value pair.
  * The list of user Data keys can be obtained by calling `/lprVehicleLists:listFields` endpoint

    Responses:
        - 200: Successfully returns information about the vehicle records
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}/vehicles"
    params = {}
    if plate is not None:
        params['plate'] = plate
    if accessType__in is not None:
        if isinstance(accessType__in, list):
            params['accessType__in'] = ','.join(map(str, accessType__in))
        else:
            params['accessType__in'] = str(accessType__in)
    if securityStatus__in is not None:
        params['securityStatus__in'] = securityStatus__in
    if userData is not None:
        params['userData'] = userData
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def add_vehicle(self, body, id):
    """Auto-generated method for 'addVehicle'

    Adds a new vehicle record to the list. This method enforces strictness about the uniqueness of vehicle license plate, so the same plate/vehicle cannot be added more than once, and would result in error if attempted.

    HTTP Method: POST
    Endpoint: /lprVehicleLists/{id}/vehicles

    Parameters:
        - id (path): Id

    Request Body:
        - body (application/json):
            Description: New record to be added.
            Required: True

    Top-level Request Body Properties:
        - validFrom (string): Date from which this record is valid
        - validTo (string): Date upto which this record is valid
        - schedule (object): It signifies a week long alert schedule. This schedule is effective according to actor's (user/camera/account) timezone. It allows setting different times for different days.

        - accessType (string): No description provided.
        - securityStatus (string): Indicates whether vehicle is
  * hotlist: Vehicle flagged for tracking
  * exempted: Vehicle is exempt from watchlist rule and other rules. This is useful, for instance, when an organization wishes to avoid alerts on known vehicles, like employee vehicles.

  * none: Empty value provided when no special consideration for the vehicle
        - userData (object): Object containing all user information associated with the specific event. For example, for a plate read, this would contain user supplied attributes for the given plate like apartment number. the following are the guidelines for supplying User Data:
  * It is recommended to use camelCase for field names, but this is not required
  * Maximum of 5 unique keys.
  * Each key or value should have only 256 characters max.
  * The keys 'type' and 'creatorId' are reserved keys.
        - plate (string): License plate number of the vehicle in uppercase

    Responses:
        - 201: Successful creation of new vehicle record
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}/vehicles"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def add_vehicles(self, body, id):
    """Auto-generated method for 'addVehicles'

    Adds multiple vehicle records to the list in a single operation. This method enforces strictness about the uniqueness of vehicle license plates. Each plate/vehicle must be unique within the list, and duplicate entries in either the request or with existing records will result in an error. 

    HTTP Method: POST
    Endpoint: /lprVehicleLists/{id}/vehicles:bulkCreate

    Parameters:
        - id (path): Id

    Request Body:
        - body (application/json):
            Description: New record to be added.
            Required: True

    Responses:
        - 201: Successful creation of new vehicle record
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}/vehicles:bulkCreate"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_vehicle(self, id, recordId):
    """Auto-generated method for 'getVehicle'

    Fetches information about a specific vehicle from a specific list

    HTTP Method: GET
    Endpoint: /lprVehicleLists/{id}/vehicles/{recordId}

    Parameters:
        - id (path): Id
        - recordId (path): Id of specific record

    Responses:
        - 200: Successfully returns information about the vehicle records
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}/vehicles/{recordId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def update_vehicle(self, body, id, recordId):
    """Auto-generated method for 'updateVehicle'

    Update given vehicle record in the given list. Specifically for the given record, create-only properties like `plate` cannot be edited. To edit those, the record would have to be deleted and a new one added.

    HTTP Method: PATCH
    Endpoint: /lprVehicleLists/{id}/vehicles/{recordId}

    Parameters:
        - id (path): Id
        - recordId (path): Id of specific record

    Request Body:
        - body (application/json):
            Description: Record to be updated.
            Required: True

    Top-level Request Body Properties:
        - validFrom (string): Date from which this record is valid
        - validTo (string): Date upto which this record is valid
        - schedule (object): It signifies a week long alert schedule. This schedule is effective according to actor's (user/camera/account) timezone. It allows setting different times for different days.

        - accessType (string): No description provided.
        - securityStatus (string): Indicates whether vehicle is
  * hotlist: Vehicle flagged for tracking
  * exempted: Vehicle is exempt from watchlist rule and other rules. This is useful, for instance, when an organization wishes to avoid alerts on known vehicles, like employee vehicles.

  * none: Empty value provided when no special consideration for the vehicle
        - userData (object): Object containing all user information associated with the specific event. For example, for a plate read, this would contain user supplied attributes for the given plate like apartment number. the following are the guidelines for supplying User Data:
  * It is recommended to use camelCase for field names, but this is not required
  * Maximum of 5 unique keys.
  * Each key or value should have only 256 characters max.
  * The keys 'type' and 'creatorId' are reserved keys.

    Responses:
        - 204: Updated the vehicle record
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}/vehicles/{recordId}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_vehicle(self, id, recordId):
    """Auto-generated method for 'deleteVehicle'

    Delete given vehicle record in given list.

    HTTP Method: DELETE
    Endpoint: /lprVehicleLists/{id}/vehicles/{recordId}

    Parameters:
        - id (path): Id
        - recordId (path): Id of specific record

    Responses:
        - 204: Deleted the record
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/lprVehicleLists/{id}/vehicles/{recordId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def search_vehicle_lists(self, plate=None, actor=None, name__contains=None, accessType__in=None, securityStatus__in=None, userData=None):
    """Auto-generated method for 'searchVehicleLists'

    Fetches the vehicle records that match search criteria, across all the lists that match the search criteria

    HTTP Method: GET
    Endpoint: /lprVehicleLists:search

    Parameters:
        - plate (query): Provide the license plate in uppercase to be searched with an exact match
        - actor (query): Filter to get only events where the actorType and actorId value equals any one of the supplied value in the list. For each entry of list, the actor type has to be prefixed along with actor id like `actorType:actorId`. For example, to filter for camera with id 100d4c41, the actorId that has to be used is `camera:100d4c41`. To search for events from a specific type of actor, for example users, use a wildcard as actorId: `user:*`.

        - name__contains (query): Phrase that is used to search for resources (rules or lists) whose names contain it
        - accessType__in (query): Search based on the access type
        - securityStatus__in (query): Filters by only those records under a specific type of security status
        - userData (query): Dynamically named query parameter that allows clients to filter events based on specific values in user supplied fields.
  * This allows searching by user supplied attributes instead of plates, for example, apartment number, organization etc.
  * If the user for example wishes to search for `organization` having value `ABC` then the correct way to search is `userData.organization=ABC`. This then needs to be specified directly in the query parameters or in json object as a key value pair.
  * The list of user Data keys can be obtained by calling `/lprVehicleLists:listFields` endpoint
        - unknown (None): No description provided

    Responses:
        - 200: Vehicle records that match the search criteria.
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = "/lprVehicleLists:search"
    params = {}
    if plate is not None:
        params['plate'] = plate
    if actor is not None:
        if isinstance(actor, list):
            params['actor'] = ','.join(map(str, actor))
        else:
            params['actor'] = str(actor)
    if name__contains is not None:
        params['name__contains'] = name__contains
    if accessType__in is not None:
        if isinstance(accessType__in, list):
            params['accessType__in'] = ','.join(map(str, accessType__in))
        else:
            params['accessType__in'] = str(accessType__in)
    if securityStatus__in is not None:
        params['securityStatus__in'] = securityStatus__in
    if userData is not None:
        params['userData'] = userData
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )
