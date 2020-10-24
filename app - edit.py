#app.py

from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import repo
import csv
import io

app = Flask(__name__)

trolleyList = list(repo.find_all())

#upload csv file
@app.route("/upload/", methods=['POST', 'GET'])
def upload_file():
    if (request.method=='POST'):
        #works to parse csv
        upfile = request.files['csvfile']
        stream = io.StringIO(upfile.stream.read().decode("UTF-8-sig"), newline=None)
        fdata = csv.reader(stream, delimiter=',')
        x = list(fdata)
        
        for item in x:
            #print(item[0])
            #print(item[1])
            #print(item[2])
            fname = item[0]
            fdate = datetime.strptime(item[1], '%Y-%m-%dT%H:%M:%S')
            ftemp = int(item[2])

            #add to db
            repo.create_recording(fname, fdate, ftemp)

            
        return redirect(url_for('create_recording'))
    return render_template("create.html", recordings=trolleyList)

@app.route("/upload/create/", methods=['POST','GET'])
def create_recording():
    if (request.method=='POST'):
        strName = request.form.get('tname')
        strDate = request.form.get('tdate')
        strTime = request.form.get('ttime')
        fTemp = request.form.get('ttemp')
        intTemp = int(fTemp)

        tdt = strDate + 'T' + strTime + ':00' #combine the date and time together because firefx is a weak browser

        dateObj = datetime.strptime(tdt, '%Y-%m-%dT%H:%M:%S')
        
        repo.create_recording(strName, dateObj, intTemp)
        return redirect(url_for('create_recording'))
        
    return render_template("create.html", recordings=trolleyList)

if __name__ == "main":
    app.run()
