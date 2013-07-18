#!/usr/bin/env python

import os
import web
from web import form
import csv
from datetime import datetime
from StringIO import StringIO
import zipfile

urls = (
        '/', 'Index',
        '/favicon.ico', 'favicon',
        '/cases', 'Cases',
        '/cases/([a-zA-Z0-9]+)', 'ShowCase',
        )

render = web.template.render('templates/')

def epoch2datetime(t):
    """Convert milliseconds from epoch to a local datetime object"""
    return datetime.fromtimestamp(t/1000.0)

class favicon(object):
    """
    On base web.py process, the request for favicon.ico 404s, this make it
    displayable and thus avoid the 404s.
    """
    def GET(self):
        raise web.redirect('static/favicon.ico')


class ShowCase(object):
    def GET(self, name):
        cases = []
        cases_dir = 'cases'
        for dirs in os.walk(cases_dir):
            cases.append(dirs)
        direc = cases[0][1]
        if not name in direc:
            message = "There's no case with the name: %s" % name
            return render.showcase(message)
        else:
            message = ''
            return render.showcase(message)


class Cases(object):

    def GET(self):
        cases = []
        cases_dir = 'cases'
        for dirs in os.walk(cases_dir):
            cases.append(dirs)
        direc = cases[0][1]
        return render.cases(direc)


class Index(object):
    """
    Class to render the index a.k.a / path of web server
    """
    def GET(self):
        return render.index()

    def POST(self):
        x = web.input(fileupload={})
        casename = x['casename']
        filepath = os.path.join(os.getcwd(), 'cases', casename)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filezip = StringIO(x['fileupload'].file.read())
        zip_list = zipfile.ZipFile(filezip, 'r')
        for item in zip_list.namelist():
            if not os.path.basename(item):
                continue
            split_name = item.split('/')[-1]
            fout = open(os.path.join(filepath, split_name), 'wb')
            fout.write(StringIO(zip_list.read(item)).read())
            fout.close()
        return web.seeother('/')

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
