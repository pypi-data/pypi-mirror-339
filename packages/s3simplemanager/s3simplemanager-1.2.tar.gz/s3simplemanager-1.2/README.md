# 1.2
* Features
    * Update functions documentations

## Example of use:

### Upload files
```
# imports
import s3simplemanager


s3 = S3SimpleManager(ssl_verification=False, bucket="s3_bucket_online", url="http://example.url.com/bucket", key_id="12345678", key_value="87654321")
s3.upload_files("example_path_local_file", "example_path_bucket_file")
for object in s3.list_files("example_path_bucket_file"):
    print(object)
```

### List files when we have a know location
```
# imports
import s3simplemanager


s3 = S3SimpleManager(ssl_verification=False, bucket="s3_bucket_online", url="http://example.url.com/bucket", key_id="12345678", key_value="87654321")
files = s3.list_files("main_folder/sub_folder")
for file in files:
    print(file)
```

### List files when we don't know the location
```
# imports
import s3simplemanager


s3 = S3SimpleManager(ssl_verification=False, bucket="s3_bucket_online", url="http://example.url.com/bucket", key_id="12345678", key_value="87654321")
files = s3.list_files()
for file in files:
    print(file)
```

### Delete files
```
# imports
import s3simplemanager


s3 = S3SimpleManager(ssl_verification=False, bucket="s3_bucket_online", url="http://example.url.com/bucket", key_id="12345678", key_value="87654321")
s3.delete_files(["main_folder_one/sub_folder_one/file_one.txt", "main_folder_two/sub_folder_two/file_two.txt"])
```
