import flask
from flask import request, jsonify
import MySQLdb
import requests
import os
import json

# 傳本地端資料到mysql，自動顯示json格式到網路上
print(os.getcwd())
path=r"./save_data"           

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False     ## json格式下，加入此行在web上才能顯示中文

def exec_query(query):
    db = MySQLdb.connect("mysql-server","root","secret","mysql") 
    cursor = db.cursor()
    try:
        cursor.execute('USE mysql')
        cursor.execute('CREATE TABLE date(date DATE, task VARCHAR(20), time DECIMAL(6,1));')
    except:
        pass

    cursor.execute(query)
    return db, cursor

query = "DROP TABLE date"
db,cursor = exec_query(query)
db.commit()
db.close()

query = "SELECT * FROM date"
db,cursor = exec_query(query)
for dates in os.listdir(path):                  #將本地端的資料上傳到mysql
    print(dates)
    with open(path+"/"+str(dates),'rb') as l:
        load_list = json.load(l)
        for task in load_list:
            print(task)
            query = "INSERT INTO date (date, task, time) VALUES ('%s','%s','%s')" % (dates[:-5], task, load_list[task])
            cursor.execute(query)
            db.commit()
db.close()


# 先創資料夾(exec_query)，再存入資料
@app.route('/', methods=['GET'])
def list_all():

    show = []    
    query = "SELECT * FROM date"
    db,cursor = exec_query(query)
    results = cursor.fetchall()
    for row in results:
        tem = {'date': row[0]}
        tem['task'] = row[1]
        tem['time'] = row[2]
        show.append(tem)
    db.close()
    print(show)

    return jsonify(show), 200

@app.route('/del', methods=["DELETE"])
def delete_all():

    db = MySQLdb.connect("mysql-server","root","secret","mysql") 
    cursor = db.cursor()
    cursor.execute("DROP TABLE date")
    db.commit()
    db.close()
    
    return '204'
    
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')