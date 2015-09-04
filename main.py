import os
import sys
import getRequest as gr
import writeMALXML as wmx
import writeXML as wx
import tarfile, StringIO, cStringIO

import time



from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, make_response

app = Flask(__name__.split('.')[0])

def addResource(zfile, url, fname):
    # get the contents
    contents = urlfetch.fetch(url).content
    # write the contents to the zip file
    zfile.writestr(fname, contents)



@app.route('/')
def index():
    return render_template('main.html')

@app.route('/submit', methods=["POST"])
def submit():
    if request.method == 'POST':
        uname =  request.form["uname"]
        method = request.form["method"]
        if method == "1":
            """Write MAL Format XML"""
            resp = gr.getRequest()
            xml = wmx.writeXML()

            xml.writeBof()

            data = resp.getInfo(uname)
            xml.write(data)

            fail = xml.writeEof()

            c = cStringIO.StringIO()
            t = tarfile.open(mode='w', fileobj=c)

            tarinfo = tarfile.TarInfo("Hummingbird-to-MAL-Export-" + (time.strftime("%m-%d-%Y")) + ".xml")
            tarinfo.size = len(xml.xmlData)
            tarinfo2 = tarfile.TarInfo("Failure-Report.xml")
            tarinfo2.size = len(fail)
            t.addfile(tarinfo, StringIO.StringIO(xml.xmlData))
            t.addfile(tarinfo2, StringIO.StringIO(fail))
            t.close()

            s = c.getvalue()

            response = make_response(s)
            response.headers["Content-Disposition"] = "attachment; filename=Hummingbird-to-MAL-Export-" + (time.strftime("%m-%d-%Y")) + ".tar"
            return response

        if method == "0":
            """Write XML using values from Hummingbird API"""
            resp = gr.getRequest()
            xml = wx.writeXML()

            xml.writeBof()

            data = resp.getInfo(uname)
            xml.write(data)

            xml.writeEof()

            response = make_response(xml.xmlData)
            response.headers["Content-Disposition"] = "attachment; filename=Hummingbird-Export-" + (time.strftime("%m-%d-%Y")) + ".xml"
            return response

    else:
        abort(401)

