import requests
from env import DB_INFO
from django.utils.crypto import get_random_string
import uuid

def request_consumer_list():
    # ret = requests.get(DB_INFO['host'] + ":" + str(DB_INFO['port']))
    ret = requests.get(DB_INFO['host'])
    if ret.status_code >= 500:
        print(ret.text, ret.status_code)
        print("[ERROR] - SERVER ISNOT STARTED !")
        return False

    # request for consumer item.
    # host = DB_INFO['host'] + ":" + str(DB_INFO['port'])
    host = DB_INFO['host']
    username = DB_INFO['username']
    password = DB_INFO['password']

    # LOGIN and get token
    payload = "{\n  \"username\": \"%s\",\n  \"pw\" : \"%s\"\n}" % (username,
                                                                    password)
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        # 'postman-token': "231f8f02-bc2a-64e0-38ec-d4b78533c854"
        }

    response = requests.request("POST",
                                host + "/api/v1_0/login/", data=payload,
                                headers=headers)
    json_response = response.json()
    if json_response['code'] != 'OK_LOGIN':
        print("[ERROR] - Login was not successfull !")
        return False
    data = json_response['data']
    token = data['token']

    # get list of consumer.
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "e3833c2b-88c4-4693-2919-5f88147d5cf8"
        }
    headers.update({'authorization': "Token {}".format(token)})
    response = requests.request("GET",
                                host + "/api/v1_0/consumer/",
                                headers=headers)

    json_response = response.json()
    if json_response['code'] != 'OK_GET':
        print("[ERROR] - Server Error.")
        print(response.text)
        return False

    list_consumers = json_response['data']
    print("Find %d consumer registered." % len(list_consumers))

    meters = {}
    for consumer in list_consumers:
        meters.update({consumer['ebs_no']: 0})

    return meters


lst = request_consumer_list()
print(lst)





