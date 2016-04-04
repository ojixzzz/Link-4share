import json
import urllib
import requests
from link4share import app
from link4share.config import cookies, client_key, client_secret
from flask import request, render_template, url_for, redirect
from pymongo import MongoClient
from requests_oauthlib import OAuth1

mongoDB = MongoClient('localhost', 27017)
dbase = mongoDB.link4share

@app.route('/generate.html', methods=['POST'])
def generate():
    try:
        link = request.form['link']
        spliturl = link.rsplit('/', 2)
        return redirect(url_for('download', idnya=spliturl[1], judul='download'))
    except Exception, e:
        return redirect(url_for('index'))

@app.route('/download/<idnya>/<judul>.html')
def download(idnya, judul):
    headers = {
        'Host': 'www.4shared.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.269 Safari/537.36'
    }

    queryoauth = OAuth1(client_key, client_secret, '', '', 
                        signature_type='query')
    url = 'https://api.4shared.com/v1_2/files/%s.json' % (idnya, )
    req = requests.get(url, auth=queryoauth)
    results = json.loads(req.text)
    if results.get('id'):
        url = results.get('downloadPage')
        req = requests.get(url, cookies=cookies, headers=headers)
        if req.text:
            haystack = req.text
            pos = haystack.find('http://dc', 0)
            if pos > 0:
                haystack = haystack[pos:]
                pos = haystack.find('"', 0)
                if pos > 0:
                    haystack = haystack[:pos]
                    directlink = True
            else:
                haystack = url
                directlink = False

            data = {
                'judul': '%s Download' % results.get('name'),
                'description': 'Direct link %s Download, at: %s' % (results.get('name'), results.get('modified')),
                'keyword': 'Direct link, %s Download, at: %s, android, iphone, 4shared' % (results.get('name'), results.get('modified')),
                'id': results.get('id'),
                'name': results.get('name'),
                'date': results.get('modified'),
                'md5': results.get('hash'),
                'size': results.get('size'),
                'download': haystack,
                'jumlah': 0,
                'directlink': directlink
            }

            filedownload = dbase.filedownload
            cursor = filedownload.find_one({"id": results.get('id')})
            if cursor:
                jumlah = cursor['jumlah'] + 1
                result = filedownload.update_one(
                    {"id": results.get('id')},
                    {"$set": {"jumlah": jumlah}}
                )
                data['jumlah'] = jumlah
            else:
                id_filedownload = filedownload.insert_one(data).inserted_id
            return render_template('download.html', data=data)

    data = {}
    return render_template('error.html', data=data), 500
