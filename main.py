from os import abort
from flask import Flask, jsonify, request
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jsonParser as parse

app = Flask(__name__)


@app.route('/parsing',methods=['GET','POST'])
def AlignRelation():
    
    if request.method == 'POST':
        if not request.json:
            print('not good formating')
            abort(400)
        json = request.json
        #parse it 
        jsonParse = parse.Parse(json)
        output = jsonParse.parseJsonRequest()
        return jsonify(output)
    elif request.method == 'GET':
        return 'Hello World from alignrelation'

if __name__ == '__main__':
    app.run(debug=True)