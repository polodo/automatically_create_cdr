from datetime import datetime, timedelta
import sys
import os
from random import random, randint, seed, choice, choices
import csv
import os.path


FILE_FORMAT_DATETIME = "%Y%m%d%H%M%S"
FILE_FORMAT_DATE = "%d/%m/%y"

METERS = {}
RANDOM_METERS = 50 # maximum random number of meters in one file
SEQUENCE_FILE = 0 # sequence
FILE_NAME = "METER_DATA_%s%s.csv"
seed(datetime.now()) # random seed

def initialize_meters(number):
    meters = {}
    for idx in range(number):
        # structure of each record will be {id : num_of_record}
        meters.update({'%0.6d' % idx : 0})
    return meters


def create_metering_file(folder_path, meters, dt):
    num_meter = randint(1, RANDOM_METERS)
    collected_meter = {k: meters[k] for k in meters if k and meters[k] <= 48}

    # random choice some meters
    old_meter = {}
    count = 0
    list_files = []
    while len(collected_meter) > len(old_meter):
        count += 1
        file_name = FILE_NAME % (dt.strftime(FILE_FORMAT_DATETIME),
                                 "%.4d" % count)
        file_name = folder_path + file_name
        if os.path.isfile(file_name):
            return False
        print("\n  --- Start create metering file : %s" % file_name)
        print("\t- List meters will be generated : %s" % str(meters.keys()))
        choice_meters = {}
        if len(collected_meter) <= num_meter:
            choice_meters = collected_meter
        else:
            for key, meter in choices(population=list(collected_meter.items()),
                                      k=num_meter):
                choice_meters.update({key: meter})
        old_meter.update(choice_meters)
        with open(file_name, 'w', newline='') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for key, meter in choice_meters.items():
                print("\t\t. Fill data for meter : %s" % key)
                # num_record = randint(0, 48 - meter)
                num_record = 48 - meter
                if num_record > 0:
                    # write the meter id line
                    spam_writer.writerow(["Meter ID: %s" % key])
                    for idx in range(num_record):
                        volt = random() * 10.0
                        data_row = [dt.strftime(FILE_FORMAT_DATE), # date
                                    meter + idx + 1, # record sequence
                                    round(volt, 4), # volt min
                                    round(volt + random() * 0.01,4), # volt max
                                    0,0
                                    ]
                        spam_writer.writerow(data_row)

        list_files.append((dt.strftime(FILE_FORMAT_DATETIME), file_name))
        print("  --- End create metering file : %s\n" % file_name)

    return list_files
