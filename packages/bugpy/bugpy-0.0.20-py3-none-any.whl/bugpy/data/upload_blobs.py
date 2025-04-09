""" Functions for uploading files to s3 """
from bugpy.utils import multithread, multiprocess
from botocore.config import Config
from functools import partial
from io import BytesIO
import pandas as pd
import boto3
import os


def _upload_one_file_tuple(file_object: tuple, bucket: str, s3_client, extension) -> None:
    """ Upload a file to an S3 bucket
    """

    filename, object_name = file_object

    ext = filename.split('.')
    if ext[-1] != extension and extension is not None:
        object = Image.open(filename)
        out_img = BytesIO()
        object.save(out_img, format=extension)
        out_img.seek(0)
        s3_client.upload_fileobj(out_img, bucket, object_name)
        return

    s3_client.upload_file(
        filename, bucket, object_name
    )


def upload_one_file(filename: str, object_name: str, bucket: str, s3_client=None, reconnect=True,
                    extension=None) -> None:
    """ Upload a file to an S3 bucket

        :param filename: File to upload
        :param bucket: Bucket to upload to
        :param object_name: s3 object name. If not specified then file_name is used
        :param s3_client: established s3 connection, autoconnects if None, defaults to None
        :param reconnect: Whether to attempt to create a new s3 session
        :type reconnect: bool

    """
    if reconnect or s3_client is None:
        session = boto3.Session()
        s3_client = session.client("s3", config=Config(max_pool_connections=os.cpu_count()),
                                   endpoint_url=os.environ['ENDPOINT'],
                                   aws_access_key_id=os.environ['API_KEY'],
                                   aws_secret_access_key=os.environ['SECRET_KEY'])

    try:
        s3_client.upload_file(
            filename, bucket, object_name
        )
    except Exception as e:
        print(f"Error in uploading {filename} to {bucket + '/' + object_name}")
        print(e)


def upload_filelist(filelist, aws_bucket, upload_dir=None, uploadnames=None, retry_attempts=50, retry=True,
                    extension=None) -> list:
    """ Uploads a list of local files

        :param filelist: iterable of image names in local storage to be uploaded
        :param aws_bucket: name of S3 bucket where images are hosted
        :param upload_dir: dir to store the images, optional
        :param uploadnames: list of directory locations/names of the uploaded images
        :param retry_attempts: number of times to retry uploads
        :param retry: retries failed uploads one time
        :return: list of files which failed to upload
    """

    config = Config(
        retries=dict(
            max_attempts=retry_attempts
        ),
        max_pool_connections=os.cpu_count()
    )
    session = boto3.Session()
    client = session.client("s3", config=config, endpoint_url=os.environ['ENDPOINT'],
                            aws_access_key_id=os.environ['API_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])

    filelist = pd.Series(filelist).dropna()

    if uploadnames is None and upload_dir is None:
        print("Please supply one of: upload_dir, uploadnames")

    if uploadnames is None and upload_dir is not None:
        uploadnames = filelist.apply(lambda col: os.path.join(upload_dir, os.path.basename(col)))

    func = partial(_upload_one_file_tuple, bucket=aws_bucket, s3_client=client, extension=extension)

    files_to_upload = filelist

    if len(files_to_upload) == 0:
        return []

    uploadnames = uploadnames.str.replace('\\', '/', regex=False)

    inputs = pd.Series(zip(files_to_upload, uploadnames))

    failed_uploads, successes = multithread(inputs, func, description="Uploading images to S3", retry=retry)

    print(f"Uploaded {len(files_to_upload) - len(failed_uploads)} images with  {len(failed_uploads)} failures.")

    return failed_uploads


def upload_one_image_from_memory(img_object, name, bucket, s3_client=None, reconnect=True, extension='auto') -> None:
    """ Upload an image from memory to an S3 bucket

        :param img_object: image object (PIL Image or np.array)
        :param name: s3 object name
        :param bucket: Bucket to upload to
        :param s3_client: established s3 connection, autoconnects if None, defaults to None
        :param reconnect: Whether to attempt to create a new s3 session
        :type reconnect: bool
        :param extension: expected file extension of image

    """

    if extension == 'auto':
        extension = name.split('.')[-1]
        if extension == 'jpg':
            extension = 'jpeg'

    if s3_client is None or reconnect:
        session = boto3.Session()
        s3_client = session.client("s3", endpoint_url=os.environ['ENDPOINT'],
                                   aws_access_key_id=os.environ['API_KEY'],
                                   aws_secret_access_key=os.environ['SECRET_KEY'])

    try:
        if type(img_object) != Image:
            img_object = Image.fromarray(img_object)
            if img_object.mode != 'RGB':
                img_object = img_object.convert('RGB')
        out_img = BytesIO()
        img_object.save(out_img, format=extension)
        out_img.seek(0)
        s3_client.upload_fileobj(out_img, bucket, name)
    except Exception as e:
        print(f"Error in uploading {name} to {bucket}")
        print(e)


def _upload_one_image_from_memory_tuple(file_object: tuple, bucket: str, s3_client, extension) -> None:
    """ Upload a file from memory to an S3 bucket """
    filename, img_object = file_object

    ext = filename.split('.')
    if ext[-1] != extension:
        filename = '.'.join(ext[:-1] + [extension])

    if type(img_object) != Image:
        img_object = Image.fromarray(img_object)
    if img_object.mode != 'RGB':
        img_object = img_object.convert('RGB')

    out_img = BytesIO()
    img_object.save(out_img, format=extension)
    out_img.seek(0)
    s3_client.upload_fileobj(out_img, bucket, filename)


def upload_images_inmemory(input_df, aws_bucket, retry=True, extension=None) -> list:
    """ Uploads a list of images in memory

        :param input_df: pandas dataframe containing at least 'object' and 'file_location'
        :param aws_bucket: name of S3 bucket where images are hosted
        :param retry: retries failed uploads one time
        :return: list of files which failed to upload
    """
    session = boto3.Session()
    client = session.client("s3", config=Config(max_pool_connections=os.cpu_count()),
                            endpoint_url=os.environ['ENDPOINT'],
                            aws_access_key_id=os.environ['API_KEY'],
                            aws_secret_access_key=os.environ['SECRET_KEY'])

    required_fields = ['object', 'file_location']
    if not all([x in input_df for x in required_fields]):
        raise Exception(
            f"Input dataframe missing one or more of the following required fields: {','.join(required_fields)}")

    input_df = input_df[['object', 'file_location']].dropna()

    if extension is None:
        extension = 'png'

    func = partial(_upload_one_image_from_memory_tuple, bucket=aws_bucket, s3_client=client, extension=extension)

    if len(input_df) == 0:
        return []

    input_df['file_location'] = input_df['file_location'].str.replace('\\', '/', regex=False)

    inputs = pd.Series(zip(input_df['file_location'], input_df['object']))

    failed_uploads, _ = multithread(inputs, func, description="Uploading in-memory images to S3", retry=retry)

    print(f"Uploaded {len(input_df) - len(failed_uploads)} images with  {len(failed_uploads)} failures.")

    return failed_uploads
