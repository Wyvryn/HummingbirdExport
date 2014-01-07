# Hummingbird Export

This app is developed in Python using Flask for Google App Engine to allow [Hummingbird](http://hummingbird.me) users to download their viewing statistics as an XML file.

See it in action at [hummingbirdexport.appengine.com](http://hummingbirdexport.appengine.com/)

##Source Notes
In getRequest.py, three variables have been ommited: apiunam, passw, and X-Mashape-Authorization. If you want to run the code locally, you'll need to add values to these fields.