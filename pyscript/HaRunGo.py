import fileinput
import requests
import json
import base64
import random

# Globle Var
file1 = open('route.data')
routes = file1.readlines()
file1.close()

file2 = open('tp.data')
tps = file2.readlines()
file2.close()

tot_cnt = len(routes)

def base16encode(username):
    return str(base64.b16encode(username))

def base64encode(username, pwd):
    list = [username, pwd]
    sign = ':'
    strr = sign.join(list)
    return "Basic " + str(base64.b64encode(strr))

def virtualDevicedId(username):
    fi = base16encode(username)
    la = username[1:]
    id = fi + la
    res = "%s-%s-%s-%s-%s" % (id[0:8], id[8:12], id[12:16], id[16:20], id[20:])
    return res

def virtualCustomDeviceId(username):
    return virtualDevicedId(username) + "_iOS_sportsWorld_campus"

def selectRoute():
    return int(random.uniform(0, tot_cnt - 1))

def login(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v3/login'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "*/*",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "appVersion",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "application/x-www-form-urlencoded",
        "DeviceId": virtualDevicedId(username),
        "CustomDeviceId": virtualCustomDeviceId(username),
        "User-Agent": "SWCampus/1.2.0 (iPhone; iOS 9.3.4; Scale/3.00)",
        "appVersion":"1.2.0"
    }

    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    reqData = Request.content
    print (reqData)
    dicData = json.loads(reqData)
    uid = dicData['data']['uid']
    return uid

def dataUpload(username, pwd, uid):
    url = 'http://gxapp.iydsj.com/api/v2/users/' + str(uid) + '/running_records/add'
    headers = {
        "appVersion": "1.2.1",
        "CustomDeviceId": virtualCustomDeviceId(username),
        "DeviceId": virtualDevicedId(username),
        "osType": "0",
        "source": "000049",
        "uid": str(uid),
        "Authorization": base64encode(username, pwd),
    }
    index = selectRoute()
    print ("Use " + str(index) + " data.")
    json = {
        "allLocJson":routes[index],
        "fivePointJson":tps[index],
        "complete": "true",
        "totalTime": 717,
        "totalDis": "1.950000",
        "stopTime": 1476900049950,
        "speed": "6.128205",
        "startTime": 1476908758891,
        "sportType": 1,
        "selDistance": 1,
        "abnormal": 0,
        "isUpload": "false",
        "unCompleteReason": 0
    }
    Session = requests.Session()
    Request = Session.post(url, headers = headers, json = json)
    print (Request.content)

def logout(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v2/user/logout'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "*/*",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "appVersion",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "application/x-www-form-urlencoded",
        "DeviceId": virtualDevicedId(username),
        "CustomDeviceId": virtualCustomDeviceId(username),
        "User-Agent": "SWCampus/1.2.0 (iPhone; iOS 9.3.4; Scale/3.00)",
        "appVersion":"1.2.0"
    }

    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    print Request.content

def writeByData():
    file = open('user.data')

    line = file.readlines()
    # for l in line:
    #     user, pwd = l.split(' ')
    #     print (base64encode(user, pwd))
    file.close()
    return line

def main():
    users = writeByData()

    for u in users:
        # username, password = u.split(' ')
        # print username, password
        # uid = login(username, password)
        # dataUpload(username, password, uid)
        # logout(username, password)


if __name__=='__main__':
    main()