import os
import sys
import getRequest as gr
import writeXML as wx
import time


from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, make_response

app = Flask(__name__.split('.')[0])


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/submit', methods=["POST"])
def submit():
    if request.method == 'POST':
        uname =  request.form["uname"]
        
        resp = gr.getRequest()
        xml = wx.writeXML()
        
        xml.writeBof()
        
        data = resp.getInfo(uname, "currently-watching")
        xml.write(data)
        
        data = resp.getInfo(uname, "completed")
        xml.write(data)
        
        data = resp.getInfo(uname, "plan-to-watch")
        xml.write(data)
        
        data = resp.getInfo(uname, "on-hold")
        xml.write(data)
        
        data = resp.getInfo(uname, "dropped")
        xml.write(data)
        
        xml.writeEof()
        
        response = make_response(xml.xmlData)
        response.headers["Content-Disposition"] = "attachment; filename=Hummingbird-Export-" + (time.strftime("%m/%d/%Y")) + ".xml"
        return response


    else:
        abort(401)

