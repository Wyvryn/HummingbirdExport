import time
import requests
import re
import redis
import logging
from hummingbirdexport.keys import redisPw, httpAuth, httpUserAgent
logging.getLogger().setLevel(logging.INFO)

class writeXML(object):

    def __init__(self):
        self.xmlData = ""
        self.fail = ""

    def writeBof(self):
        self.xmlData += '<?xml version="1.0" encoding="UTF-8" ?>\n'
        self.xmlData += '\t<myanimelist>\n\n'
        self.xmlData += '\t\t<myinfo>\n'
        self.xmlData += '\t\t\t<user_id>3467089</user_id>\n'
        self.xmlData += '\t\t\t<user_name>wyvdev</user_name>\n'
        self.xmlData += '\t\t\t<user_export_type>1</user_export_type>\n'
        self.xmlData += '\t\t\t<user_total_anime>0</user_total_anime>\n'
        self.xmlData += '\t\t\t<user_total_watching>0</user_total_watching>\n'
        self.xmlData += '\t\t\t<user_total_completed>0</user_total_completed>\n'
        self.xmlData += '\t\t\t<user_total_onhold>0</user_total_onhold>\n'
        self.xmlData += '\t\t\t<user_total_dropped>0</user_total_dropped>\n'
        self.xmlData += '\t\t\t<user_total_plantowatch>0</user_total_plantowatch>\n'
        self.xmlData += '\t\t</myinfo>\n\n'
        self.fail += '<?xml version="1.0" encoding="UTF-8" ?>\n'
        self.fail += '\t<myanimelist>\n\n'

    def write(self, data):
        for i in data:
            from hummingbirdexport.keys import r
            res = redis.StrictRedis(host=r['host'], port=r['port'], db=r['db'],
                password = redisPw)
            malid = res.get(i['anime']['title'].encode('utf8'))

            if not malid:
                title = i['anime']['title'].encode('utf8')
                title = title.strip()
                title = title.replace(" ", "%20")
                url = "http://myanimelist.net/api/anime/search.xml?q=%s" % title
                headers = {
                    'Authorization': httpAuth,
                    'User-Agent': httpUserAgent}
                r = requests.get(url, headers=headers)
                try:
                    x = re.compile(".*<id>").split(r.text.encode('utf8'))
                    y = re.compile("</id>.*").split(x[1])
                    malid = y[0]
                except:
                    logging.warn("Couldn't find id for %s" % i['anime']['title'])

                if malid:
                    logging.info("Addind %s with id %s" % (i['anime']['title'].encode('utf8'), malid))
                    res.set(i['anime']['title'].encode('utf8'), int(malid))

            if malid:
                self.xmlData += "\t\t<anime>\n"

                self.xmlData += "\t\t\t<series_animedb_id>"

                self.xmlData += malid
                self.xmlData += "</series_animedb_id>\n"

                self.xmlData += "\t\t\t<series_title>"
                if i['anime']['title']:

                    self.xmlData += "<![CDATA[" + i[
                        'anime']['title'].encode('utf8') + "]]>"
                self.xmlData += "</series_title>\n"

                self.xmlData += "\t\t\t<series_type></series_type>\n"
                self.xmlData += "\t\t\t<series_episodes></series_episodes>\n"
                self.xmlData += "\t\t\t<my_id>0</my_id>\n"

                self.xmlData += "\t\t\t<my_watched_episodes>"
                if i['episodes_watched']:
                    self.xmlData += str(i['episodes_watched'])
                self.xmlData += "</my_watched_episodes>\n"

                self.xmlData += "\t\t\t<my_start_date></my_start_date>\n"
                self.xmlData += "\t\t\t<my_finish_date></my_finish_date>\n"
                self.xmlData += "\t\t\t<my_rated></my_rated>\n"

                self.xmlData += "\t\t\t<my_score>"
                if i['rating']['value']:
                    self.xmlData += str(int(float(i['rating']['value']) * 2))
                self.xmlData += "</my_score>\n"

                self.xmlData += "\t\t\t<my_dvd></my_dvd>\n"
                self.xmlData += "\t\t\t<my_storage></my_storage>\n"

                self.xmlData += "\t\t\t<my_status>"
                if i['status']:
                    if i['status'] == 'currently-watching':
                        self.xmlData += "Watching"
                    elif i['status'] == 'completed':
                        self.xmlData += "Completed"
                    elif i['status'] == 'plan-to-watch':
                        self.xmlData += 'Plan to Watch'
                    elif i['status'] == 'on-hold':
                        self.xmlData += 'On-Hold'
                    elif i['status'] == 'dropped':
                        self.xmlData += 'Dropped'
                    else:
                        self.xmlData += ""
                self.xmlData += "</my_status>\n"

                self.xmlData += "\t\t\t<my_comments>"
                self.xmlData += "<![CDATA["
                if i['notes']:
                    self.xmlData += i['notes'].encode('utf8')
                self.xmlData += "]]></my_comments>\n"

                self.xmlData += "\t\t\t<my_times_watched>"
                if i['rewatched_times']:
                    self.xmlData += str(i['rewatched_times'] + 1)
                else:
                    self.xmlData += "1"
                self.xmlData += "</my_times_watched>\n"

                self.xmlData += "\t\t\t<my_rewatch_value></my_rewatch_value>\n"
                self.xmlData += "\t\t\t<my_downloaded_eps>0</my_downloaded_eps>\n"
                self.xmlData += "\t\t\t<my_tags><![CDATA[]]></my_tags>\n"

                self.xmlData += "\t\t\t<my_rewatching></my_rewatching>\n"
                self.xmlData += "\t\t\t<my_rewatching_ep>0</my_rewatching_ep>\n"
                self.xmlData += "\t\t\t<update_on_import>1</update_on_import>\n"

                self.xmlData += "\t\t</anime>\n\n"
            else:
                self.fail += "\t\t<anime>\n"
                self.fail += "\t\t\t<series_title>"
                if i['anime']['title']:
                    self.fail += "<![CDATA[" + i['anime']['title'].encode('utf8') + "]]>"
                self.fail += "</series_title>\n"

                self.fail += "\t\t\t<id>"
                if i['id']:
                    self.fail += str(i['id'])
                self.fail += "</id>\n"

                self.fail += "\t\t\t<series_type>"
                if i['anime']['show_type']:
                    self.fail += i['anime']['show_type'].encode('utf8')
                self.fail += "</series_type>\n"

                self.fail += "\t\t\t<series_episodes>"
                if i['anime']['episode_count']:
                    self.fail += str(i['anime']['episode_count'])
                self.fail += "</series_episodes>\n"

                self.fail += "\t\t\t<my_watched_episodes>"
                if i['episodes_watched']:
                    self.fail += str(i['episodes_watched'])
                self.fail += "</my_watched_episodes>\n"

                self.fail += "\t\t\t<my_score>"
                if i['rating']['value']:
                    self.fail += str(float(i['rating']['value']) * 2)
                self.fail += "</my_score>\n"

                self.fail += "\t\t\t<my_status>"
                if i['status']:
                    self.fail += i['status'].encode('utf8')
                self.fail += "</my_status>\n"

                self.fail += "\t\t\t<my_times_watched>"
                if i['rewatched_times']:
                    self.fail += str(i['rewatched_times'])
                self.fail += "</my_times_watched>\n"

                self.fail += "\t\t\t<my_comments>"
                if i['notes']:
                    self.fail += "<![CDATA[" + i['notes'].encode('utf8') + "]]>"
                self.fail += "</my_comments>\n"

                self.fail += "\t\t\t<last_watched>"
                if i['last_watched']:
                    self.fail += i['last_watched'].encode('utf8')
                self.fail += "</last_watched>\n"

                self.fail += "\t\t</anime>\n\n"

    def writeEof(self):
        self.xmlData += '\t</myanimelist>\n\n'
        self.fail += '\t</myanimelist>\n\n'
        return self.fail
