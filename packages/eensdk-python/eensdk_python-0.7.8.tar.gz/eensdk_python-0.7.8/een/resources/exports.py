def create_export_job(self, body):
    """Auto-generated method for 'createExportJob'

    Creates and starts a new video export job

    HTTP Method: POST
    Endpoint: /exports

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Responses:
        - 201: Created
        - 400: The supplied object is invalid. Error detail will contain the validation error.
        - 401: You are not authenticated. Please authenticate and try again.
        - 403: You have no permission to access the specified resource.
        - 404: Referenced resource could not be found.
        - 500: Something went wrong in the server. Please try again.
    """
    endpoint = "/exports"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )


def retry_export(self, body, jobId):
    """Auto-generated method for 'retryExport'

    Start the export again with minor changes of some of the original parameters, which are specified in the body of the api.
Fields that are not given will be kept the same as the original job.
Failed intervals are tried again, adding a suffix to the names of the generated mp4's to indicate they are created by a retry.


    HTTP Method: POST
    Endpoint: /exports/{jobId}:copy

    Parameters:
        - jobId (path): ID of the export job.

    Request Body:
        - body (application/json):
            Description: No description provided.
            Required: True

    Top-level Request Body Properties:
        - retryStrategy (string): Strategy to use to decide what to export
* full: export all files just as the original export
* failedIntervalsFully: for each file that had a failed interval, retry the whole file
* minimal: only retry the parts that failed


    Responses:
        - 201: Created
        - 400: No description provided
        - 401: No description provided
        - 403: No description provided
        - 404: No description provided
        - 415: Content type of request body not supported.
        - 500: No description provided
    """
    endpoint = f"/exports/{jobId}:copy"
    params = None
    data = body
    return self._api_call(
        endpoint=endpoint,
        method='POST',
        params=params,
        data=data,
    )
