import pymysql
import os
import json
import requests

# read JSON file which is in the next parent folder
file_path = os.path.realpath(os.path.join(
    os.getcwd(), 'taipei-attractions.json'))

json_data = open(file_path, "r", encoding="utf-8")
json_obj = json.load(json_data)


# do validation and checks before insert
def validate_string(val):
    if val != None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


# connect to MySQL
con = pymysql.connect(host='localhost', user='kevin',
                     passwd='T@kevin1', db='website')
#con = pymysql.connect(host='localhost', user='root',
#                      passwd='nn101586501', db='website')
cursor = con.cursor()


# parse json data to SQL insert
for i, item in enumerate(json_obj["result"]["results"]):
    SERIAL_NO = validate_string(item["SERIAL_NO"])
    RowNumber = validate_string(item["RowNumber"])
    info = validate_string(item["info"])
    stitle = validate_string(item["stitle"])
    longitude = validate_string(item["longitude"])
    latitude = validate_string(item["latitude"])
    jsonImagePath = validate_string("http" + item["file"].split("http")[1])
    #filePath = validate_string("http" + item["file"].split("http")[1])
    address = validate_string(item["address"])
    langinfo = validate_string(item["langinfo"])
    MRT = validate_string(item["MRT"])
    CAT1 = validate_string(item["CAT1"])
    CAT2 = validate_string(item["CAT2"])
    MEMO_TIME = validate_string(item["MEMO_TIME"])
    REF_WP = validate_string(item["REF_WP"])
    POI = validate_string(item["POI"])
    idpt = validate_string(item["idpt"])
    xbody = validate_string(item["xbody"].replace("\'", "\\'"))
    _id = int(item["_id"])
    xpostDate = validate_string(item["xpostDate"])
    avBegin = validate_string(item["avBegin"])
    avEnd = validate_string(item["avEnd"])

    # 檢查DB是否已存在該筆資料
    searchSql = "SELECT SERIAL_NO FROM attractions WHERE SERIAL_NO = '"+SERIAL_NO+"'"
    # print(searchSql)
    cursor.execute(searchSql)
    has_data = cursor.fetchone()

    # 若已存在就跳過
    if has_data:
        print(has_data[0])
        continue

    # 將圖片下載至本機電腦，透過語法儲存在DB
    url = jsonImagePath
    r = requests.get(url)

    host = "18.224.68.14:3000"
    image_name = str(_id)

    pysicalPath = "/var/www/html/taipei-day-trip-website/static/images/{0}-0.jpg".format(image_name)

    with open(pysicalPath, 'wb') as f:
        f.write(r.content)

    filePath = "http://{0}/static/images/{1}-0.jpg".format(
        host, image_name)

    # 若無誤，就執行插入DB語法
    insertSql = "INSERT INTO attractions (SERIAL_NO, RowNumber, info, stitle, longitude, latitude, file, address, langinfo, MRT, CAT1, CAT2, MEMO_TIME, REF_WP, POI, idpt, xbody, _id, xpostDate, avBegin, avEnd) " + \
        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', {17}, '{18}', '{19}', '{20}')".format(
            SERIAL_NO, RowNumber, info, stitle, longitude, latitude, filePath, address, langinfo, MRT, CAT1, CAT2, MEMO_TIME, REF_WP, POI, idpt, xbody, _id, xpostDate, avBegin, avEnd)
    print(insertSql)
    cursor.execute(insertSql)
    con.commit()
    # break

con.close()
