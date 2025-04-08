# imports
import boto3
import os


class S3SimpleManager:
    def __init__(self, ssl_verification: bool = False, bucket: str = "", url: str = "", key_id: str = "", key_value: str = "") -> None:
        self.bucket_name = bucket
        self.endpoint_url = url
        self.access_key_id = key_id
        self.secret_access_key = key_value
        self.s3_session = boto3.client("s3", aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_access_key, endpoint_url=self.endpoint_url, verify=ssl_verification)

    # Getters
    def get_bucket_name(self) -> str:
        """
        This function will fetch the s3 bucket name
        :return:
            - bucket_name - Bucket name in a string
        """
        return self.bucket_name
    
    def get_endpoint_url(self) -> str:
        """
        This function will fetch the url of the s3 bucket
        :return:
            - endpoint_url - String text to get the enpoint of the bucket
        """
        return self.endpoint_url
    
    def get_access_key_id(self) -> str:
        """
        This function will fetch the access key id
        :return:
            - access_key_id - Access key id in a string text
        """
        return self.access_key_id
    
    def get_secret_access_key(self) -> str:
        """
        This function will fetch the secret access key
        :return:
            - secret_access_key - Secret access key in a string
        """
        return self.secret_access_key

    # Setters
    def set_bucket_name(self, bucket: str) -> None:
        self.bucket_name = bucket
    
    def set_endpoint_url(self, url: str) -> None:
        self.endpoint_url = url
    
    def set_access_key_id(self, key_id: str) -> None:
        self.access_key_id = key_id
    
    def set_secret_access_key(self, secret: str) -> None:
        self.secret_access_key = secret
    
    # Methods
    def upload_files(self, local_file_path: str, bucket_file_path: str) -> None:
        """
        This function will upload the file passed by <local_loaction> to s3 bucket in the destination folder <bucket_location>
        :param str local_file_path: File local path (this path must exists)
        :param str bucket_file_path: Bucket path where to store the file (this path will be created automatically)
        :return:
        """
        if os.path.exists(local_file_path):
            if os.path.isfile(local_file_path):
                self.s3_session.upload_file(f"{local_file_path}", self.bucket_name, f"{bucket_file_path}")

    def list_files(self, location: str = "") -> list:
        """
        This fuction list all files inside a s3 bucket.
        :param str location: string value that will have the file location inside s3 bucket. If left empty all Content inside the bucket will be printed.
        :return:
            - objects - list of objects inside the bucket 
        """
        objects = []

        if location == "":
            for object in self.s3_session.list_objects(Bucket=self.bucket_name)['Contents']:
                objects.append(object)

            return objects
        else:
            for object in self.s3_session.list_objects(Bucket=self.bucket_name)['Contents']:
                if location in object['Key']:
                    objects.append(object)
            
            return objects
    
    def delete_files(self, locations: list) -> None:
        """
        This fuction will delete the files passed by the var <locations>.
        :param list locations: list that contains all the files to be deleted.
        :return:
        """
        for object in locations:
            self.s3_session.delete_object(Bucket=self.bucket_name, Key=object)
