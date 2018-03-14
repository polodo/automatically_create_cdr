import sched
import time

from datetime import datetime, timedelta
from connect_db import request_consumer_list
from generate_metering_files import create_metering_file
from upload_file_to_S3 import upload_to_s3

count = 0
meters = {}
AWS3_FOLDER_PATH = 'data/storage'
while 1:
    print("============= START A CYCLE =============")
    if count % 4 == 0:
        # connect to get new consumer every hours
        print("************ UPDATE METER LIST ****************")
        meters = request_consumer_list()
        print("************ END UPDATING METER LIST **********")
    if meters:
        lst_files = create_metering_file('', meters,
                                         datetime.today() + timedelta(days=count))
        if lst_files:
            # upload to AWS3
            for f in lst_files:
                upload_to_s3(AWS3_FOLDER_PATH, f[0], f[1])
    print("============= END A CYCLE =============")
    time.sleep(15 * 60)
    count += 1

