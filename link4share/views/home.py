from link4share import app
from flask import render_template, url_for
from slugify import slugify
from pymongo import MongoClient
from random import randrange

mongoDB = MongoClient('localhost', 27017)
dbase = mongoDB.link4share

@app.route('/')
def index():
    files = []
    cursor = dbase.filedownload.find().sort([("jumlah", -1)]).limit(5)
    for document in cursor:
        nameslug = slugify(document['name'], separator="_")
        url = url_for('download', idnya=document['id'], judul=nameslug)
        file = {
            "name": document['name'],
            "date": document['date'],
            "size": document['size'],
            "url": url,
            "jumlah": document['jumlah']
        }
        files.append(file)

    data = {
        'judul': 'Home',
        'description': 'Link-4shared.com is the download link generator sites from 4share. that does not provide files in',
        'keyword': 'download, direct 4share,',
        'files': files
    }
    return render_template('home.html', data=data)

@app.route('/random.html')
def random_page():
    files = []
    count  = dbase.filedownload.count()
    for x in range(0, 9):
        offset = randrange( 0, count )
        document = dbase.filedownload.find().skip( offset ).limit(1)[0]
        nameslug = slugify(document['name'], separator="_")
        url = url_for('download', idnya=document['id'], judul=nameslug)
        file = {
            "name": document['name'],
            "date": document['date'],
            "size": document['size'],
            "url": url,
            "jumlah": document['jumlah']
        }
        files.append(file)

    data = {
        'judul': 'Random page',
        'description': '',
        'keyword': '',
        'files': files
    }
    return render_template('random_page.html', data=data)


@app.route('/recent.html')
def recent_page():
    files = []
    cursor = dbase.filedownload.find().sort([("$natural", -1)]).limit(10)
    for document in cursor:
        nameslug = slugify(document['name'], separator="_")
        url = url_for('download', idnya=document['id'], judul=nameslug)
        file = {
            "name": document['name'],
            "date": document['date'],
            "size": document['size'],
            "url": url,
            "jumlah": document['jumlah']
        }
        files.append(file)

    data = {
        'judul': 'Recent page',
        'description': '',
        'keyword': '',
        'files': files
    }
    return render_template('recent_page.html', data=data)

@app.route('/disclaimer.html')
def disclaimer():
    data = {
        'judul': 'Disclaimer',
        'description': '',
        'keyword': '',
    }
    return render_template('disclaimer.html', data=data)