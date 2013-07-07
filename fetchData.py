import MySQLdb
import json
con = MySQLdb.connect(host='192.168.3.105', db='nozomi', user='root', passwd='badperson', charset='utf8')
res = []
for i in xrange(5, 15):
    sql = 'select * from nozomi_text where `key` = "dataAchieveTitle%d"' % (i)
    con.query(sql)
    title = con.store_result().fetch_row(0, 1)[0]
    cn = title['chinese']
    eng = title['english']

    sql = 'select * from nozomi_text where `key`="dataAchieveDesc%d_1"' % (i)
    con.query(sql)
    desc1 = con.store_result().fetch_row(0, 1)[0]
    engDes1 = desc1["english"]

    sql = 'select * from nozomi_text where `key`="dataAchieveDesc%d_2"' % (i)
    con.query(sql)
    desc2 = con.store_result().fetch_row(0, 1)[0]
    engDes2 = desc2["english"]

    sql = 'select * from nozomi_text where `key`="dataAchieveDesc%d_3"' % (i)
    con.query(sql)
    desc3 = con.store_result().fetch_row(0, 1)[0]
    engDes3 = desc3["english"]
    res.append([cn, eng, engDes1, engDes2, engDes3])

print json.dumps(res)


