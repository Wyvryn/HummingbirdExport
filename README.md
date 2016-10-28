# Hummingbird Export

This app is developed in Python 3 using Flask to allow [Hummingbird](http://hummingbird.me) users to download their viewing statistics as an XML file.

Experimental functionality has been added to create an XML file that is importable on [MyAnimeList](http://myanimelist.net).

To run locally, populate the data in `hummingbirdexport/config.py.template` and save it as `hummingbirdexport/config.py`.

Run `make env` to build the virtualenv, `source ./env/bin/activate` to activate the virtualenv, and finally `python manage.py runserver`

See it in action at [http://hummingbird.illyasviel.moe/](http://hummingbird.illyasviel.moe/)

##License
Code is licensed under CC BY-SA 4.0
http://creativecommons.org/licenses/by-sa/4.0/
http://creativecommons.org/licenses/by-sa/4.0/legalcode
