__author__ = 'Mike'
import urllib
import urllib2
import re

import xml.etree.ElementTree as ET

class findAID(object):
    def __init__(self):
        self.dict = {}

    def getAID(self):
        tree = ET.parse('./malval.xml')
        root = tree.getroot()

        for anime in root.findall('anime'):
            titles = anime.findall('title')
            for t in titles:
                self.dict[t.text] = anime.get('aid')

    def addToDb(self, title):
        print title
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()

        """
        The MyAnimeList api requires a valid user and password for authentication before
        returning any data. For ease of use I have created an account to do this, rather than
        have a user input their personal username and password. 
        """
        passman.add_password(None, "http://myanimelist.net/api/anime/", "", "")
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

        req = urllib2.Request("http://myanimelist.net/api/anime/search.xml?q=" + urllib.quote(title))
        f = urllib2.urlopen(req)
        data = f.read()
        x = re.compile(".*<id>").split(data)
        y = re.compile("</id>.*").split(x[1])
        txt = "\t<anime aid=\"" + y[0] + "\">\n\t\t<title>" + title + "</title>\n\t</anime>\n</malids>"

        readFile = open("./malval.xml")
        lines = readFile.readlines()
        readFile.close()

        w = open("./malval.xml",'w')
        w.writelines([item for item in lines[:-1]])
        w.write(txt)
        w.close()

    def lookup(self, title):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        """
        The MyAnimeList api requires a valid user and password for authentication before
        returning any data. For ease of use I have created an account to do this, rather than
        have a user input their personal username and password. 
        """
        passman.add_password(None, "http://myanimelist.net/api/anime/", "", "")
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

        req = urllib2.Request("http://myanimelist.net/api/anime/search.xml?q=" + urllib.quote(title))
        f = urllib2.urlopen(req)
        if f.getcode == 200:
            data = f.read()
            x = re.compile(".*<id>").split(data)
            y = re.compile("</id>.*").split(x[1])
            return y[0]
        else:
            return ""