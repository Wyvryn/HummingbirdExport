import time

class writeXML(object):

    def __init__(self):
        self.xmlData = ""
    
    def writeBof(self):
        self.xmlData += '<?xml version="1.0" encoding="UTF-8" ?>\n'
        self.xmlData += '<!--\n'
        self.xmlData += 'Created using Wyvryn\'s Hummingbird Exporter\nhttp://hummingbirdexport.appspot.com/\n'
        self.xmlData += (time.strftime("%m/%d/%Y"))
        self.xmlData += '\n-->\n\n'
        
        self.xmlData += '\t<hummingbird>\n\n'
        
    def write(self, data):
        for i in data:
            self.xmlData += "\t\t<anime>\n"
    
            self.xmlData += "\t\t\t<series_title>"
            if i['anime']['title']:
                self.xmlData += i['anime']['title'].encode('utf8')
            self.xmlData += "</series_title>\n"
            
            self.xmlData += "\t\t\t<id>"
            if i['id']:
                self.xmlData += str(i['id'])
            self.xmlData += "</id>\n"
            
            self.xmlData += "\t\t\t<series_type>"
            if i['anime']['show_type']:
                self.xmlData += i['anime']['show_type'].encode('utf8')
            self.xmlData += "</series_type>\n"
            
            self.xmlData += "\t\t\t<series_episodes>"
            if i['anime']['episode_count']:
                self.xmlData += str(i['anime']['episode_count'])
            self.xmlData += "</series_episodes>\n"
            
            self.xmlData += "\t\t\t<my_watched_episodes>"
            if i['episodes_watched']:
                self.xmlData += str(i['episodes_watched'])
            self.xmlData += "</my_watched_episodes>\n"
            
            self.xmlData += "\t\t\t<my_score>"
            if i['rating']['value']:
                self.xmlData += i['rating']['value'].encode('utf8')
            self.xmlData += "</my_score>\n"
            
            self.xmlData += "\t\t\t<my_status>"
            if i['status']:
                self.xmlData += i['status'].encode('utf8')
            self.xmlData += "</my_status>\n"
            
            self.xmlData += "\t\t\t<my_times_watched>"
            if i['rewatched_times']:
                self.xmlData += str(i['rewatched_times'])
            self.xmlData += "</my_times_watched>\n"
            
            self.xmlData += "\t\t\t<my_notes>"
            if i['notes']:
                self.xmlData += i['notes'].encode('utf8')
            self.xmlData += "</my_notes>\n"
            
            self.xmlData += "\t\t\t<my_notes_present>"
            if i['notes_present']:
                self.xmlData += i['notes_present'].encode('utf8')
            self.xmlData += "</my_notes_present>\n"
            
            self.xmlData += "\t\t\t<last_watched>"
            if i['last_watched']:
                self.xmlData += i['last_watched'].encode('utf8')
            self.xmlData += "</last_watched>\n"
             
            self.xmlData += "\t\t</anime>\n\n"
        
        
    def writeEof(self):
        self.xmlData += '\t</hummingbird>\n\n'
        