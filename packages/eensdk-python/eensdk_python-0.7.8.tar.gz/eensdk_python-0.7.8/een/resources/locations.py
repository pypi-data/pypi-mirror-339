def get_locations(self, include=None, sort=None, pageToken=None, pageSize=None, parentId=None, parentId__ne=None, parentId__in=None, name=None, name__ne=None, name__in=None, name__contains=None, address_streetAddress=None, address_streetAddress__ne=None, address_streetAddress__in=None, address_streetAddress__contains=None, address_streetAddress2=None, address_streetAddress2__ne=None, address_streetAddress2__in=None, address_streetAddress2__contains=None, address_city=None, address_city__ne=None, address_city__in=None, address_city__contains=None, address_region=None, address_region__ne=None, address_region__in=None, address_region__contains=None, address_country=None, address_country__ne=None, address_country__in=None, address_country__contains=None, address_postalCode=None, address_postalCode__ne=None, address_postalCode__in=None, address_postalCode__contains=None, childLocationCount=None, childLocationCount__ne=None, q=None, qRelevance__gte=None):
    """Auto-generated method for 'getLocations'

    This endpoint is used to retrieve a list of locations. Support for Location-based camera grouping is only available in the professional and enterprise editions.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available locations, not the number of locations resulting from the query string.


    HTTP Method: GET
    Endpoint: /locations

    Parameters:
        - include (query): List of properties that should be included in the response
        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=8 - Only eight values will be accepted, more will return error 400
 * qRelevance is optional ordering parameter which is available if q filter is used, if q filter is not passed qRelevance as ordering parameter will return error 400

        - pageToken (query): Token string value that references a page for pagination. This value is received when retrieving the first page in the `nextPageToken` and `prevPageToken` fields.

        - pageSize (query): The number of entries to return per page. The maximum range of valid page sizes is documented with minimum and  maximum values, but the range might be further limited dynamically based on the requested information, account, and system status. Values outside of the (dynamic) allowed range will not result in an error, but will be clamped to the nearest limit. Thus, logic to detect the last page should not be based on comparing the requested size with the received size, but on the existence of a `nextPageToken` value.

        - parentId (query): Filter to get the locations with the specified parentId. parentId=null returns only the locations which do not have a parent location
        - parentId__ne (query): Filter to get the locations with the parentId that is not equal to the provided value. The lookup is exact and case insensitive
        - parentId__in (query): Filter to get the locations whose parentId is on the provided list. The lookup is exact and case insensitive
        - name (query): Filter to get the locations with the specified name. The lookup is exact and case insensitive
        - name__ne (query): Filter to get the locations with the name that is not equal to the provided value. The lookup is exact and case insensitive
        - name__in (query): Filter to get the locations whose name is on the provided list. The lookup is exact and case insensitive
        - name__contains (query): Filter to get the locations whose the name contains the provided substring. The lookup is exact and case insensitive

        - address.streetAddress (query): Filter to get the locations with the specified address.streetAddress. The lookup is exact and case insensitive
        - address.streetAddress__ne (query): Filter to get the locations with an address.streetAddress that is not equal to the provided value. The lookup is exact and case insensitive
        - address.streetAddress__in (query): Filter to get the locations whose address.streetAddress is on the provided list. The lookup is exact and case insensitive
        - address.streetAddress__contains (query): Filter to get the locations whose the address.streetAddress contains the provided substring. The lookup is exact and case insensitive

        - address.streetAddress2 (query): Filter to get the locations with the specified address.streetAddress2. The lookup is exact and case insensitive
        - address.streetAddress2__ne (query): Filter to get the locations with an address.streetAddress2 that is not equal to the provided value. The lookup is exact and case insensitive
        - address.streetAddress2__in (query): Filter to get the locations whose address.streetAddress2 is on the provided list. The lookup is exact and case insensitive
        - address.streetAddress2__contains (query): Filter to get the locations whose the address.streetAddress2 contains the provided substring. The lookup is exact and case insensitive

        - address.city (query): Filter to get the locations with the specified address.city. The lookup is exact and case insensitive
        - address.city__ne (query): Filter to get the locations with an address.city that is not equal to the provided value. The lookup is exact and case insensitive
        - address.city__in (query): Filter to get the locations whose address.city is on the provided list. The lookup is exact and case insensitive
        - address.city__contains (query): Filter to get the locations whose the address.city contains the provided substring. The lookup is exact and case insensitive

        - address.region (query): Filter to get the locations with the specified address.region. The lookup is exact and case insensitive
        - address.region__ne (query): Filter to get the locations with an address.region that is not equal to the provided value. The lookup is exact and case insensitive
        - address.region__in (query): Filter to get the locations whose address.region is on the provided list. The lookup is exact and case insensitive
        - address.region__contains (query): Filter to get the locations whose the address.region contains the provided substring. The lookup is exact and case insensitive

        - address.country (query): Filter to get the locations with the specified address.country. The lookup is exact and case insensitive
        - address.country__ne (query): Filter to get the locations with an address.country that is not equal to the provided value. The lookup is exact and case insensitive
        - address.country__in (query): Filter to get the locations whose address.country is on the provided list. The lookup is exact and case insensitive
        - address.country__contains (query): Filter to get the locations whose the address.country contains the provided substring. The lookup is exact and case insensitive

        - address.postalCode (query): Filter to get the locations with the specified address.postalCode. The lookup is exact and case insensitive
        - address.postalCode__ne (query): Filter to get the locations with an address.postalCode that is not equal to the provided value. The lookup is exact and case insensitive
        - address.postalCode__in (query): Filter to get the locations whose address.postalCode is on the provided list. The lookup is exact and case insensitive
        - address.postalCode__contains (query): Filter to get the locations whose the address.postalCode contains the provided substring. The lookup is exact and case insensitive

        - childLocationCount (query): Filter to get the locations with the specified number of direct children
        - childLocationCount__ne (query): Filter to get the locations with the number of direct children not equal to the provided value.
        - q (query): Text search that is applied to multiple fields. The fields being searched are defined by the backend and can be changed without warning. Example fields being searched: `name`, `id`, `notes`.

        - qRelevance__gte (query): Sets the current minimum similarity threshold that is used with the `q` parameter. The threshold must be between 0 and 1 (float, default is 0.5).


    Responses:
        - 200: Successfully fetched
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/locations"
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
    if parentId is not None:
        params['parentId'] = parentId
    if parentId__ne is not None:
        params['parentId__ne'] = parentId__ne
    if parentId__in is not None:
        if isinstance(parentId__in, list):
            params['parentId__in'] = ','.join(map(str, parentId__in))
        else:
            params['parentId__in'] = str(parentId__in)
    if name is not None:
        params['name'] = name
    if name__ne is not None:
        params['name__ne'] = name__ne
    if name__in is not None:
        if isinstance(name__in, list):
            params['name__in'] = ','.join(map(str, name__in))
        else:
            params['name__in'] = str(name__in)
    if name__contains is not None:
        params['name__contains'] = name__contains
    if address_streetAddress is not None:
        params['address_streetAddress'] = address_streetAddress
    if address_streetAddress__ne is not None:
        params['address_streetAddress__ne'] = address_streetAddress__ne
    if address_streetAddress__in is not None:
        if isinstance(address_streetAddress__in, list):
            params['address_streetAddress__in'] = ','.join(map(str, address_streetAddress__in))
        else:
            params['address_streetAddress__in'] = str(address_streetAddress__in)
    if address_streetAddress__contains is not None:
        params['address_streetAddress__contains'] = address_streetAddress__contains
    if address_streetAddress2 is not None:
        params['address_streetAddress2'] = address_streetAddress2
    if address_streetAddress2__ne is not None:
        params['address_streetAddress2__ne'] = address_streetAddress2__ne
    if address_streetAddress2__in is not None:
        if isinstance(address_streetAddress2__in, list):
            params['address_streetAddress2__in'] = ','.join(map(str, address_streetAddress2__in))
        else:
            params['address_streetAddress2__in'] = str(address_streetAddress2__in)
    if address_streetAddress2__contains is not None:
        params['address_streetAddress2__contains'] = address_streetAddress2__contains
    if address_city is not None:
        params['address_city'] = address_city
    if address_city__ne is not None:
        params['address_city__ne'] = address_city__ne
    if address_city__in is not None:
        if isinstance(address_city__in, list):
            params['address_city__in'] = ','.join(map(str, address_city__in))
        else:
            params['address_city__in'] = str(address_city__in)
    if address_city__contains is not None:
        params['address_city__contains'] = address_city__contains
    if address_region is not None:
        params['address_region'] = address_region
    if address_region__ne is not None:
        params['address_region__ne'] = address_region__ne
    if address_region__in is not None:
        if isinstance(address_region__in, list):
            params['address_region__in'] = ','.join(map(str, address_region__in))
        else:
            params['address_region__in'] = str(address_region__in)
    if address_region__contains is not None:
        params['address_region__contains'] = address_region__contains
    if address_country is not None:
        params['address_country'] = address_country
    if address_country__ne is not None:
        params['address_country__ne'] = address_country__ne
    if address_country__in is not None:
        if isinstance(address_country__in, list):
            params['address_country__in'] = ','.join(map(str, address_country__in))
        else:
            params['address_country__in'] = str(address_country__in)
    if address_country__contains is not None:
        params['address_country__contains'] = address_country__contains
    if address_postalCode is not None:
        params['address_postalCode'] = address_postalCode
    if address_postalCode__ne is not None:
        params['address_postalCode__ne'] = address_postalCode__ne
    if address_postalCode__in is not None:
        if isinstance(address_postalCode__in, list):
            params['address_postalCode__in'] = ','.join(map(str, address_postalCode__in))
        else:
            params['address_postalCode__in'] = str(address_postalCode__in)
    if address_postalCode__contains is not None:
        params['address_postalCode__contains'] = address_postalCode__contains
    if childLocationCount is not None:
        params['childLocationCount'] = childLocationCount
    if childLocationCount__ne is not None:
        params['childLocationCount__ne'] = childLocationCount__ne
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


def create_location(self, body=None):
    """Auto-generated method for 'createLocation'

    This endpoint allows you to create a new location. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: POST
    Endpoint: /locations

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - id (string): Unique identifier of the resource
        - name (string): No description provided.
        - parentId (string): Unique identifier of this location's parent location in the hierarchy
        - isDefault (boolean): Specifies if a new device should be automatically assigned to this location if not supplied

        - address (object): No description provided.
        - notes (string): Description for the location
        - geometry (object): GeoJSON structure to store polygon for the specific location.
Currently the only supported geometry type is MultiPolygon, but in the future more GeoJSON schemas might be supported, so clients should be able to handle unknown schemas.

This field must be in the standard GeoJSON format, as described in https://datatracker.ietf.org/doc/html/rfc7946

Please read https://datatracker.ietf.org/doc/html/rfc7946 for more information about the GeoJSON standard.

        - childLocationCount (integer): The total count of direct children of the location
        - effectivePermissions (object): No description provided.
        - resourceCounts (object): Count of resources.
        - resourceStatusCounts (object): Count of resources by status.

    Responses:
        - 201: Location created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: Referenced resource could not be found.
        - 500: No description provided
    """
    endpoint = "/locations"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_location(self, id, include=None):
    """Auto-generated method for 'getLocation'

    This endpoint allows retrieval of the location with a specific ID. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: GET
    Endpoint: /locations/{id}

    Parameters:
        - id (path): Location ID
        - include (query): List of properties that should be included in the response

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{id}"
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


def update_location(self, id, body=None):
    """Auto-generated method for 'updateLocation'

    This endpoint allows you to update the location with the given ID. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: PATCH
    Endpoint: /locations/{id}

    Parameters:
        - id (path): Location ID

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - id (string): Unique identifier of the resource
        - name (string): No description provided.
        - parentId (string): Unique identifier of this location's parent location in the hierarchy
        - isDefault (boolean): Specifies if a new device should be automatically assigned to this location if not supplied

        - address (object): No description provided.
        - notes (string): Description for the location
        - geometry (object): GeoJSON structure to store polygon for the specific location.
Currently the only supported geometry type is MultiPolygon, but in the future more GeoJSON schemas might be supported, so clients should be able to handle unknown schemas.

This field must be in the standard GeoJSON format, as described in https://datatracker.ietf.org/doc/html/rfc7946

Please read https://datatracker.ietf.org/doc/html/rfc7946 for more information about the GeoJSON standard.

        - childLocationCount (integer): The total count of direct children of the location
        - effectivePermissions (object): No description provided.
        - resourceCounts (object): Count of resources.
        - resourceStatusCounts (object): Count of resources by status.

    Responses:
        - 204: Location updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_location(self, id):
    """Auto-generated method for 'deleteLocation'

    This endpoint allows you to delete the location with the given ID. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: DELETE
    Endpoint: /locations/{id}

    Parameters:
        - id (path): Location ID

    Responses:
        - 204: Location deleted
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_location_descendants(self, id, include=None, sort=None, parentId=None, parentId__ne=None, parentId__in=None, name=None, name__ne=None, name__in=None, name__contains=None, address_streetAddress=None, address_streetAddress__ne=None, address_streetAddress__in=None, address_streetAddress__contains=None, address_streetAddress2=None, address_streetAddress2__ne=None, address_streetAddress2__in=None, address_streetAddress2__contains=None, address_city=None, address_city__ne=None, address_city__in=None, address_city__contains=None, address_region=None, address_region__ne=None, address_region__in=None, address_region__contains=None, address_country=None, address_country__ne=None, address_country__in=None, address_country__contains=None, address_postalCode=None, address_postalCode__ne=None, address_postalCode__in=None, address_postalCode__contains=None, childLocationCount=None, childLocationCount__ne=None):
    """Auto-generated method for 'getLocationDescendants'

    This endpoint allows you to retrieve the (grand) children of the location with the given ID. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: GET
    Endpoint: /locations/{id}/locations

    Parameters:
        - id (path): Location ID
        - include (query): List of properties that should be included in the response
        - sort (query): Comma separated list of of fields that should be sorted.
 * `sort=` - not providing any value will result in error 400
 * `sort=+name,+name` - same values will result in error 400
 * `sort=-name,+name` - mutially exclusive values will return error 400
 * maxItem=8 - Only eight values will be accepted, more will return error 400

        - unknown (None): No description provided
        - parentId (query): Filter to get the locations with the specified parentId. parentId=null returns only the locations which do not have a parent location
        - parentId__ne (query): Filter to get the locations with the parentId that is not equal to the provided value. The lookup is exact and case insensitive
        - parentId__in (query): Filter to get the locations whose parentId is on the provided list. The lookup is exact and case insensitive
        - name (query): Filter to get the locations with the specified name. The lookup is exact and case insensitive
        - name__ne (query): Filter to get the locations with the name that is not equal to the provided value. The lookup is exact and case insensitive
        - name__in (query): Filter to get the locations whose name is on the provided list. The lookup is exact and case insensitive
        - name__contains (query): Filter to get the locations whose the name contains the provided substring. The lookup is exact and case insensitive

        - address.streetAddress (query): Filter to get the locations with the specified address.streetAddress. The lookup is exact and case insensitive
        - address.streetAddress__ne (query): Filter to get the locations with an address.streetAddress that is not equal to the provided value. The lookup is exact and case insensitive
        - address.streetAddress__in (query): Filter to get the locations whose address.streetAddress is on the provided list. The lookup is exact and case insensitive
        - address.streetAddress__contains (query): Filter to get the locations whose the address.streetAddress contains the provided substring. The lookup is exact and case insensitive

        - address.streetAddress2 (query): Filter to get the locations with the specified address.streetAddress2. The lookup is exact and case insensitive
        - address.streetAddress2__ne (query): Filter to get the locations with an address.streetAddress2 that is not equal to the provided value. The lookup is exact and case insensitive
        - address.streetAddress2__in (query): Filter to get the locations whose address.streetAddress2 is on the provided list. The lookup is exact and case insensitive
        - address.streetAddress2__contains (query): Filter to get the locations whose the address.streetAddress2 contains the provided substring. The lookup is exact and case insensitive

        - address.city (query): Filter to get the locations with the specified address.city. The lookup is exact and case insensitive
        - address.city__ne (query): Filter to get the locations with an address.city that is not equal to the provided value. The lookup is exact and case insensitive
        - address.city__in (query): Filter to get the locations whose address.city is on the provided list. The lookup is exact and case insensitive
        - address.city__contains (query): Filter to get the locations whose the address.city contains the provided substring. The lookup is exact and case insensitive

        - address.region (query): Filter to get the locations with the specified address.region. The lookup is exact and case insensitive
        - address.region__ne (query): Filter to get the locations with an address.region that is not equal to the provided value. The lookup is exact and case insensitive
        - address.region__in (query): Filter to get the locations whose address.region is on the provided list. The lookup is exact and case insensitive
        - address.region__contains (query): Filter to get the locations whose the address.region contains the provided substring. The lookup is exact and case insensitive

        - address.country (query): Filter to get the locations with the specified address.country. The lookup is exact and case insensitive
        - address.country__ne (query): Filter to get the locations with an address.country that is not equal to the provided value. The lookup is exact and case insensitive
        - address.country__in (query): Filter to get the locations whose address.country is on the provided list. The lookup is exact and case insensitive
        - address.country__contains (query): Filter to get the locations whose the address.country contains the provided substring. The lookup is exact and case insensitive

        - address.postalCode (query): Filter to get the locations with the specified address.postalCode. The lookup is exact and case insensitive
        - address.postalCode__ne (query): Filter to get the locations with an address.postalCode that is not equal to the provided value. The lookup is exact and case insensitive
        - address.postalCode__in (query): Filter to get the locations whose address.postalCode is on the provided list. The lookup is exact and case insensitive
        - address.postalCode__contains (query): Filter to get the locations whose the address.postalCode contains the provided substring. The lookup is exact and case insensitive

        - childLocationCount (query): Filter to get the locations with the specified number of direct children
        - childLocationCount__ne (query): Filter to get the locations with the number of direct children not equal to the provided value.

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{id}/locations"
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
    if parentId is not None:
        params['parentId'] = parentId
    if parentId__ne is not None:
        params['parentId__ne'] = parentId__ne
    if parentId__in is not None:
        if isinstance(parentId__in, list):
            params['parentId__in'] = ','.join(map(str, parentId__in))
        else:
            params['parentId__in'] = str(parentId__in)
    if name is not None:
        params['name'] = name
    if name__ne is not None:
        params['name__ne'] = name__ne
    if name__in is not None:
        if isinstance(name__in, list):
            params['name__in'] = ','.join(map(str, name__in))
        else:
            params['name__in'] = str(name__in)
    if name__contains is not None:
        params['name__contains'] = name__contains
    if address_streetAddress is not None:
        params['address_streetAddress'] = address_streetAddress
    if address_streetAddress__ne is not None:
        params['address_streetAddress__ne'] = address_streetAddress__ne
    if address_streetAddress__in is not None:
        if isinstance(address_streetAddress__in, list):
            params['address_streetAddress__in'] = ','.join(map(str, address_streetAddress__in))
        else:
            params['address_streetAddress__in'] = str(address_streetAddress__in)
    if address_streetAddress__contains is not None:
        params['address_streetAddress__contains'] = address_streetAddress__contains
    if address_streetAddress2 is not None:
        params['address_streetAddress2'] = address_streetAddress2
    if address_streetAddress2__ne is not None:
        params['address_streetAddress2__ne'] = address_streetAddress2__ne
    if address_streetAddress2__in is not None:
        if isinstance(address_streetAddress2__in, list):
            params['address_streetAddress2__in'] = ','.join(map(str, address_streetAddress2__in))
        else:
            params['address_streetAddress2__in'] = str(address_streetAddress2__in)
    if address_streetAddress2__contains is not None:
        params['address_streetAddress2__contains'] = address_streetAddress2__contains
    if address_city is not None:
        params['address_city'] = address_city
    if address_city__ne is not None:
        params['address_city__ne'] = address_city__ne
    if address_city__in is not None:
        if isinstance(address_city__in, list):
            params['address_city__in'] = ','.join(map(str, address_city__in))
        else:
            params['address_city__in'] = str(address_city__in)
    if address_city__contains is not None:
        params['address_city__contains'] = address_city__contains
    if address_region is not None:
        params['address_region'] = address_region
    if address_region__ne is not None:
        params['address_region__ne'] = address_region__ne
    if address_region__in is not None:
        if isinstance(address_region__in, list):
            params['address_region__in'] = ','.join(map(str, address_region__in))
        else:
            params['address_region__in'] = str(address_region__in)
    if address_region__contains is not None:
        params['address_region__contains'] = address_region__contains
    if address_country is not None:
        params['address_country'] = address_country
    if address_country__ne is not None:
        params['address_country__ne'] = address_country__ne
    if address_country__in is not None:
        if isinstance(address_country__in, list):
            params['address_country__in'] = ','.join(map(str, address_country__in))
        else:
            params['address_country__in'] = str(address_country__in)
    if address_country__contains is not None:
        params['address_country__contains'] = address_country__contains
    if address_postalCode is not None:
        params['address_postalCode'] = address_postalCode
    if address_postalCode__ne is not None:
        params['address_postalCode__ne'] = address_postalCode__ne
    if address_postalCode__in is not None:
        if isinstance(address_postalCode__in, list):
            params['address_postalCode__in'] = ','.join(map(str, address_postalCode__in))
        else:
            params['address_postalCode__in'] = str(address_postalCode__in)
    if address_postalCode__contains is not None:
        params['address_postalCode__contains'] = address_postalCode__contains
    if childLocationCount is not None:
        params['childLocationCount'] = childLocationCount
    if childLocationCount__ne is not None:
        params['childLocationCount__ne'] = childLocationCount__ne
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_location_floors(self, locationId, include=None):
    """Auto-generated method for 'getLocationFloors'

    This endpoint allows you to retrieve the floors at the given location. Support for Location-based camera grouping is only available in the professional and enterprise editions.
It is important to note that after using the pageSize parameter, the "totalSize" in the response represents the total number of available floors, not the number of floors resulting from the query string.


    HTTP Method: GET
    Endpoint: /locations/{locationId}/floors

    Parameters:
        - locationId (path): Location ID
        - unknown (None): No description provided
        - include (query): List of properties that should be included in the response

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors"
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


def create_floor(self, locationId, body=None):
    """Auto-generated method for 'createFloor'

    This endpoint allows you to create a floor. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: POST
    Endpoint: /locations/{locationId}/floors

    Parameters:
        - locationId (path): Location ID

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - id (string): Unique identifier of the floor
        - name (string): No description provided.
        - floorLevel (integer): The floor level in a multi-storey building
        - topLeftCoordinates (object): No description provided.
        - bottomRightCoordinates (object): No description provided.
        - floorPlans (array): No description provided.

    Responses:
        - 201: Floor created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 409: There was a conflict while trying to perform your request. See error details for more information.
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def get_floor(self, locationId, id, include=None):
    """Auto-generated method for 'getFloor'

    This endpoint allows you to retrieve a specific floor at a specific location. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: GET
    Endpoint: /locations/{locationId}/floors/{id}

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID
        - include (query): List of properties that should be included in the response

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}"
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


def update_floor(self, locationId, id, body=None):
    """Auto-generated method for 'updateFloor'

    Updates one or more fields of the given floor. This has no effect on the cameras on that floor. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: PATCH
    Endpoint: /locations/{locationId}/floors/{id}

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: False

    Top-level Request Body Properties:
        - id (string): Unique identifier of the floor
        - name (string): No description provided.
        - floorLevel (integer): The floor level in a multi-storey building
        - topLeftCoordinates (object): No description provided.
        - bottomRightCoordinates (object): No description provided.
        - floorPlans (array): No description provided.

    Responses:
        - 204: Floor updated
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='PATCH',
        params=params,
        data=data,
    )


def delete_floor(self, locationId, id):
    """Auto-generated method for 'deleteFloor'

    This endpoint allows you to delete a specific floor of a specific location. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: DELETE
    Endpoint: /locations/{locationId}/floors/{id}

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID

    Responses:
        - 204: Floor deleted
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )


def get_floor_image(self, locationId, id, type):
    """Auto-generated method for 'getFloorImage'

    This endpoint allows you to retrieve the floor image of a specific floor. Please first check the floorPlans field in GET /locations/{locationId}/floors or GET /locations/{locationId}/floors/{id} to see if a file with this format exists. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: GET
    Endpoint: /locations/{locationId}/floors/{id}.{type}

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID
        - type (path): Type of the floor image

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}.{type}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def get_floor_plans(self, locationId, id):
    """Auto-generated method for 'getFloorPlans'

    This endpoint allows you to retrieve plans of a specific floor at a specific location. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: GET
    Endpoint: /locations/{locationId}/floors/{id}/plans

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID
        - unknown (None): No description provided

    Responses:
        - 200: Successfully fetched
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}/plans"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='GET',
        params=params,
        data=data,
    )


def set_floor_plan(self, locationId, id, body=None):
    """Auto-generated method for 'setFloorPlan'

    This endpoint allows you to create a floor plan for a specific floor at a specific location. Currently only one floor plan file is supported per floor, which means that uploading a new file will overwrite any existing file, even if it has a different format (svg vs png). Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: POST
    Endpoint: /locations/{locationId}/floors/{id}/plans

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID

    Request Body:
        - body (multipart/form-data):
            Description: 
            Required: False

    Responses:
        - 201: Successfully set
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}/plans"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def delete_floor_plan(self, locationId, id, planId):
    """Auto-generated method for 'deleteFloorPlan'

    This endpoint allows you to delete a floor plan and its corresponding SVG or PNG file. Support for Location-based camera grouping is only available in the professional and enterprise editions.


    HTTP Method: DELETE
    Endpoint: /locations/{locationId}/floors/{id}/plans/{planId}

    Parameters:
        - locationId (path): Location ID
        - id (path): Floor ID
        - planId (path): Plan ID

    Responses:
        - 204: Floor plan deleted
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 500: No description provided
    """
    endpoint = f"/locations/{locationId}/floors/{id}/plans/{planId}"
    params = None
    data = None
    return self._api_call(
        endpoint=endpoint,
        method='DELETE',
        params=params,
        data=data,
    )
