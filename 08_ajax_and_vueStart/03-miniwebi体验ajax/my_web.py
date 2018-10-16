import re
from pymysql import *
import urllib.parse
import json

'''
g_url_func = {
    "/index.py": index,
    "/center.py": center
}
'''


class web():
    g_url_func = dict()

    def __init__(self):
        self.db = connect(host="127.0.0.1",
                          port=3306,
                          user="demouser",
                          password='demopassword',
                          database="stock_db",
                          charset='utf8')

        # get object of Cursor
        self.cursor = db.cursor()

    def route(self, url):
        def set_func(func):
            # key: /index.py
            # value: index
            self.g_url_func[url] = func

            def call_func():
                func()

            return call_func()

        return set_func

    def close_mysql(self):
        self.cursor.close()
        self.db.close()

    # ajax接口
    @route(r"/index_data")
    def index(self, file_name, url_param=None, url=None):
        sql = ''' select * from info;'''
        self.cursor.execute(sql)
        data_from_mysql = self.cursor.fetchall()

        jsonData = []

        for row in data_from_mysql:
            result = {}
            result['id'] = str(row[0])
            result['code'] = str(row[1])
            result['sname'] = str(row[2])
            result['rate01'] = str(row[3])
            result['rate02'] = str(row[4])
            result['new_prize'] = str(row[5])
            result['high'] = str(row[6])
            result['date'] = str(row[7])
            jsonData.append(result)

        content = json.dumps(jsonData)
        return content

    # jsonp接口
    @route(r"/index_jsonp_data")
    def index_jsonp(self, file_name, url_param, url=None):
        # callback=jQuery1124018787969015631711_1522330247607&_1522330247608
        dat_arr = re.split('[=&]]', url_param)
        fnName = dat_arr[1]

        sql = ''' select * from info; '''
        self.cursor.execute(sql)
        data_from_mysql = self.cursor.fetchall()

        jsonData = []

        for row in data_from_mysql:
            result = {}
            result['id'] = str(row[0])
            result['code'] = str(row[1])
            result['sname'] = str(row[2])
            result['rate01'] = str(row[3])
            result['rate02'] = str(row[4])
            result['new_prize'] = str(row[5])
            result['high'] = str(row[6])
            result['date'] = str(row[7])
            jsonData.append(result)

        content = json.dumps(jsonData)
        content += fnName + '(' + str(content) + ')'
        return content

    # ajax接口
    @route(r"/center_data")
    def center(self, file_name, url_param=None, url=None):
        # data_from_mysql = "this my databases's data"
        sql = ''' select i.code, i.short, i.chg, i.turnover, i.price,i.highs, f.note_info from info as i inner join focus as f on f.info_id=i.id;'''
        self.cursor.execute(sql)
        data_from_mysql = self.cursor.fetchall()

        jsonData = []
        for row in data_from_mysql:
            result = {}
            result['code'] =        str(row[0])
            result['sname'] =       str(row[1])
            result['rate01'] =      str(row[2])
            result['rate02'] =      str(row[3])
            result['new_prize'] =   str(row[4])
            result['high'] =        str(row[5])
            result['bak'] =         str(row[6])
            jsonData.append(result)

        content = json.dumps(jsonData)
        return content
