import os
from flask import Flask, render_template
from flask import request
from crypt import methods
import pymysql
import datetime
import pytz

# creates a Flask application named app 
app = Flask(__name__)

connection = pymysql.connect(host='week8project.cx929pf3iq7u.ap-southeast-1.rds.amazonaws.com',
                             user='admin',
                             password='12345678',
                             database='chat',
                             port=3306)


host = os.uname()[1]


def convertTuple(tup):
        # initialize an empty string
    string_converted = ''
    for item in tup:
        string_converted = string_converted + str(item) + " "
    return string_converted


# a route where we display the template
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/chat/<room>")
def main(room):
    return render_template('index.html')


@app.route("/<room>")
def main2(room):
    return render_template('index.html')


@app.route("/api/chat/<room>", methods=['POST', 'GET'])
def chat(room):
    dbs = None
    if request.method == 'POST':
        tz_hcm = pytz.timezone('Asia/Ho_Chi_Minh')
        start_utc = datetime.datetime.now(tz_hcm)
        time_now = start_utc.strftime("%Y-%m-%d %X")
        username = request.form['username']
        messages = request.form['msg']
        cur = connection.cursor()
        cur.execute(''' INSERT INTO chat1(room, time_now, username, msg) VALUES (%s,%s,%s,%s)''', (room,time_now,username,messages))
        cur.connection.commit()
        cur.close()
        return ''
    else:
        cur = connection.cursor()
        cur.execute(''' SELECT * FROM chat1 WHERE room=%s ''', (room,))
        dbs = cur.fetchall()
        str_result = 'Load balancing server: ' + host + "\n\n"
        for line in dbs:
            str_result = str_result + convertTuple(line) + '\n'
        cur.close()
        return str_result


# run the application
if __name__ == "__main__":
    app.run()
