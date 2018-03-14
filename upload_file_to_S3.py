
from boto3.session import Session
from datetime import datetime


AWS_ACCESS_KEY_ID = 'AKIAIYBYVKS3RYEBFTBQ'
AWS_SECRET_ACCESS_KEY = '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'
region='us-east-1'
CANONICAL_USER_ID = '300d08de1a5b2a7196ceacbb3f1620b0d6f6f4597728660880e94504eceb437e'
BUCKET = "sse-meter-reading-test"


def parse_filename_to_folder_path(root_path, file_name):
    folder_path = root_path
    fmt = "%Y%m%d%H%M%S"
    dt = datetime.strptime(file_name, fmt)
    if dt:
        year = dt.strftime("%Y")
        month = dt.strftime("%B")
        day = dt.strftime("%d")
        folder_path = root_path + "/" if root_path else ""
        folder_path = folder_path + "/".join([year, month, day])
    # return folder_path, 'usage_data_test.csv'
    return folder_path and folder_path + '/' + 'usage_data.csv' or None


def upload_to_s3(root_path, parse_string, local_fp):
    client = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    aws_file_name = parse_filename_to_folder_path(root_path, parse_string)
    s3 = client.client('s3')
    obj = s3.upload_file(local_fp,
                         BUCKET,
                         aws_file_name,
                         ExtraArgs={'ACL': 'public-read-write'})
    return True
