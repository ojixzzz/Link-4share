Link-4share
============

link4-share.com adalah situs premium link download generator dari situs 4shared

`Link-4share` ditulis dalam bahasa pemrograman python, demo site [Link-4share.com](https://link-4share.com).

-------------------

link4-share.com is a premium site generator download link from the site 4shared.

`Link-4share` is written in python language, demo site [Link-4share.com](https://link-4share.com).

Installation
------------

	- clone
	- install dependency (pip install -r requirements.txt)
	- install mongodb
	- copy config.py.sample to config.py
	- client_key & secret? goto http://www.4shared.com/developer/docs/
	- cookies = copy from browser

Run
-----
	gunicorn runserver:app