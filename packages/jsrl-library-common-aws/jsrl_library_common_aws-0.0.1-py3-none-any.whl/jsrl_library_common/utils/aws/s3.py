import re
import uuid
import boto3
from botocore import exceptions as botocore_exceptions
from functools import partial
from botocore.config import Config
from jsrl_library_common.constants.aws import s3_constants as s3_cnts
from jsrl_library_common.exceptions.aws import s3_exceptions as aws_exceptions

def list_files(s3_path,
               s3_client=None,
               server_side_encryption=False):
    """List all files into the s3 bucket

    Args:
        - s3_path: the s3 bucket path
        - s3_client (boto3.client): the s3 client if exists
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?

    Returns:
        - list: the files obtained
        - boto3.client: the s3 client
    """
    client = _get_s3_connection(server_side_encryption,
                                s3_client)
    bucket, s3_object_path = _get_s3_path(s3_path)
    response = client.list_objects_v2(Bucket=bucket,
                                      Prefix=s3_object_path)
    join_s3_path = partial(_join_s3_path,
                           bucket=bucket)
    files = list(map(lambda item: join_s3_path(item["Key"]),
                     response.get("Contents", [])))
    while (response.get("NextContinuationToken", None) is not None):
        response = client.list_objects_v2(Bucket=bucket,
                                          Prefix=s3_object_path,
                                          ContinuationToken=response["NextContinuationToken"])
        new_files = list(map(lambda item: join_s3_path(item["Key"]),
                             response.get("Contents", [])))
        files.extend(new_files)
    return files, client


def list_objects(bucket,
                 prefix=None,
                 delimiter=None,
                 s3_client=None,
                 server_side_encryption=None):
    """Get the object list from s3 based on the delimiter attribute

    Args:
        - bucket (str): the bucket name
        - delimiter (str): the objects to seek
        - s3_client (boto3.client): the s3 client if exists
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?

    Returns:
        - list: the object paths
        - boto3.client: the s3 client
    """
    files = set()
    folders = set()
    client = _get_s3_connection(server_side_encryption,
                                s3_client)
    flag = True
    parameters = {"Bucket": bucket}
    if prefix:
        parameters["Prefix"] = prefix
    if delimiter:
        parameters["Delimiter"] = delimiter

    while flag:
        response = client.list_objects_v2(**parameters)
        folders = folders.union([resource["Prefix"] for resource in response.get("CommonPrefixes", [])])
        files = files.union([resource["Key"] for resource in response.get("Contents", [])])
        if response.get("NextContinuationToken", None):
            parameters["ContinuationToken"] = response["NextContinuationToken"]
        else:
            flag = False

    return files, folders, client
    

def get_object_content(bucket,
                       object_path,
                       s3_client=None,
                       server_side_encryption=None):
    """Get file content from s3

    Args:
        - bucket (str): the bucket name
        - object_path (str): the object path into the s3 bucket
        - s3_client (boto3.client): the s3 client if exists
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?

    Returns:
        - list: the object paths
        - boto3.client: the s3 client
    """
    s3_client = _get_s3_connection(server_side_encryption=server_side_encryption,
                                   s3_client=s3_client)
    response = s3_client.get_object(Bucket=bucket,
                                    Key=object_path)
    response = response["Body"].read()
    return response, s3_client


def check_object_exist(bucket,
                       object_path,
                       get_object=True,
                       s3_client=None,
                       server_side_encryption=None):
    """Check if object exists in s3 bucket

    Args:
        - bucket (str): the bucket name
        - object_path (str): the object path into the s3 bucket
        - get_object (bool, optional): should the object be returned?. Defaults to True.
        - s3_client (boto3.client, optional): the s3 client if exists. Defaults to None.
        - server_side_encryption (bool, optional): does the server side activate the AWS signature v4 (s3v4)?. Defaults to None.

    Returns:
        - bytes|None: the object content
        - boto3.client: the s3 client
    """
    response = b''
    s3_client = _get_s3_connection(server_side_encryption=server_side_encryption,
                                   s3_client=s3_client)
    try:
        if get_object:
            response, _ = get_object_content(bucket,
                                            object_path,
                                            s3_client=s3_client)
        else:
            s3_client.get_object(Bucket=bucket,
                                 Key=object_path)
    except botocore_exceptions.ClientError:
        response = None

    return response, s3_client


def check_bucket_existance(bucket,
                           s3_client=None,
                           server_side_encryption=None):
    """Validate if bucket exists in s3

    Args:
        - bucket (str): the bucket name
        - s3_client (boto3.client): the s3 client if exists
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?

    Returns:
        - dict: the AWS response
        - boto3.client: the s3 client
    """
    try:
        s3_client = _get_s3_connection(server_side_encryption=server_side_encryption,
                                       s3_client=s3_client)
    
        response = s3_client.head_bucket(Bucket=bucket)
        return response, s3_client
    except botocore_exceptions.ClientError:
        raise aws_exceptions.BucketNotExist(f"The bucket {bucket} doesn't exist or you are not have permissions")


def upload_file_with_object_name(filename,
                                 bucket,
                                 object_name,
                                 s3_client=None,
                                 server_side_encryption=False):
    """Upload file to s3
    
    Args:
        - filename (str): the file name to upload
        - bucket (str): the s3 bucket where file will be upload
        - object_name (str): the root with name of s3 file
        - s3_client (boto3.client): the s3 client if exists
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?
        
    Returns:
        - boto3.client: the s3 client    
    """
    client = _get_s3_connection(server_side_encryption,
                                s3_client)

    with open(filename, "rb") as file:
        client.upload_fileobj(file, 
                              bucket,
                              object_name)
        
    return client


def put_file(bucket,
             object_path,
             content,
             s3_client=None,
             server_side_encryption=False):
    """Modify the file content

    Args:
        - bucket (str): the s3 bucket where file will be upload
        - object_name (str): the path of s3 file
        - content (str): the file content
        - s3_client (boto3.client): the s3 client if exists
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?
        
    Returns:
        - boto3.client: the s3 client
    """
    client = _get_s3_connection(server_side_encryption,
                                s3_client)
    if type(content) is str:
        content = content.encode()
    client.put_object(Body=content,
                      Bucket=bucket,
                      Key=object_path)
    
    return client


def create_presigned_url(s3_file,
                         expiration,
                         filename,
                         mimetype,
                         server_side_encryption=False,
                         s3_client=None):
    """Create a presigned url to s3 client

    Args:
        - s3_file (string): the complete s3 of file
        - expiration (int): the number of seconds before access was closed
        - filename (string): the response file name
        - mimetype (string): the mime type of response file
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?
        - s3_client (boto3.client): the s3 client if exists

    Returns:
        - string: the url presigned
    """
    bucket, object_path = _get_s3_path(s3_file)
    client = _get_s3_connection(server_side_encryption,
                                s3_client)
    params = {
        'Bucket': bucket,
        'Key': object_path,
        "ResponseContentDisposition": f"attachment; filename={filename}",
        "ResponseContentType": mimetype
    }
    response = client.generate_presigned_url('get_object',
                                             Params=params,
                                             ExpiresIn=expiration)
    return response


def generate_presigned_post(bucket,
                            filename,
                            expires_in=3600,
                            server_side_encryption=False,
                            s3_client=None):
    """Create a presigned url to s3 client to upload files to S3 bucket

    Args:
        - bucket (string): The name of the bucket to which the files are to be uploaded.
        - filename (string): A key is a unique identifier to a file
        - expires_in (int): value in seconds
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?
        - s3_client (boto3.client): the s3 client if exists

    Returns:
        - dict: A dictionary with two elements: url and fields. Url is the url to post to.
                Fields is a dictionary filled with the form fields and respective values
                to use when submitting the post.
    """

    client = _get_s3_connection(server_side_encryption,
                                s3_client)
    response = client.generate_presigned_post(Bucket=bucket,
                                              Key=filename,
                                              ExpiresIn=expires_in)
    return response


def generate_temporal_client(aws_access_key_id,
                             aws_secret_access_key,
                             aws_session_token,
                             server_side_encryption=False):
    """Generate a temporal s3 client

    Args:
        - aws_access_key_id (str): the temporal access key id
        - aws_secret_access_key (str): the temporal secret access key
        - aws_session_token (str): the session token
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?

    Returns:
        - boto3.client: the s3 client
    """
    params = {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_session_token": aws_session_token
    }

    if server_side_encryption:
        params["config"] = Config(signature_version='s3v4')

    return boto3.client('s3', **params)


def _get_s3_path(s3_path):
    """Extract the bucket and path of s3 resource

    Args:
        - s3_path: the full path of s3 resource

    Returns:
        - str: the bucket name
        - str: the s3 resource path
    """
    s3_resources = re.match(r"s3://(?P<bucket>(.(?!/))*.)/(?P<path>.*)",
                            s3_path).groupdict()
    return s3_resources["bucket"], \
           s3_resources["path"]


def _join_s3_path(object_key,
                  bucket):
    """Create the s3 path from object key (file path without bucket segment)
    and the bucket where is located

    Args:
        - object_key (str): the file path without bucket segment
        - bucket (str): the bucket where is located the object

    Returs:
        - str: the full s3 path
    """
    return _join_path(f"s3://{bucket}", object_key)


def _join_path(path,
               *paths):
    """Join one or more path segments

    Args:
        - path (str): the path
        - *paths (str tuple): the path segments to concatenate
                                 NOTE: the number of paths must be greater or equal than 1

    Returns:
        - str: the new path
    """
    if not len(paths): 
        raise aws_exceptions.EmptyJoinPathSegments()
    new_path = s3_cnts.SEP.join(paths) if (path[-1] == s3_cnts.SEP) \
                               else s3_cnts.SEP + s3_cnts.SEP.join(paths)
    return path + new_path


def _get_s3_connection(server_side_encryption=False,
                       s3_client=None):
    """Get the s3 connection

    Args:
        - server_side_encryption (bool): does the server side activate the AWS signature v4 (s3v4)?
        - s3_client (boto3.client): the s3 client if exists

    Returns:
        - boto3.client: the s3 client
    """
    client = None
    if (s3_client):
        client = s3_client
    else: 
        if (server_side_encryption):
            client = boto3.client('s3',
                                  config=Config(signature_version='s3v4'))
        else:
            client = boto3.client('s3')
    return client


def _get_random_name():
    """Create a random name based on the uuid

    Returns:
        - string: the random name
    """
    return str(uuid.uuid4())
