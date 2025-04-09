import boto3

def assume_role(role,
                role_session_name,
                duration=None,
                sts_client=None):
    """Generate a temporal credentials

    Args:
        - role (str): the role arn
        - role_session_name (str): the name of the session
        - duration (int): the session duration in seconds
        - sts_client (boto3.client): the sts client if exists

    Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html
        
    Returns:
        - dict: the sts assume role response
        - boto3.client: the sts client
    """
    client = _get_sts_connection(sts_client)
    params = {
        "RoleArn": role,
        "RoleSessionName": role_session_name
    }
    if duration:
        params["DurationSeconds"] = duration

    response = client.assume_role(**params)
    return response, client



def _get_sts_connection(sts_client=None):
    """Get the s3 connection

    Args:
        - sts_client (boto3.client): the sts client if exists

    Returns:
        - boto3.client: the sts client
    """
    client = None
    if (sts_client):
        client = sts_client
    else: 
        client = boto3.client('sts')
    return client