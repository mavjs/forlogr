#!/usr/bin/env python

import os
import web
import csv
from datetime import datetime
from StringIO import StringIO
import zipfile
from readinfo import (
        infoxml,
        calllog,
        )

urls = (
        '/', 'Index',
        '/favicon.ico', 'favicon',
        '/cases', 'Cases',
        '/cases/([a-zA-Z0-9]+)', 'ShowCase',
        '/cases/Mateen/CallLog', 'CallLog',
        '/cases/([a-zA-Z0-9]+)/BrowserSearches/', 'BrowserSearches',
        '/cases/([a-zA-Z0-9]+)/CallLog/', 'CallLog',
        '/cases/([a-zA-Z0-9]+)/Contacts/', 'Contacts',
        '/cases/([a-zA-Z0-9]+)/Media/', 'Media',
        '/cases/([a-zA-Z0-9]+)/MMSAttachments/', 'MMSAttachments',
        '/cases/([a-zA-Z0-9]+)/MMS/', 'MMS',
        '/cases/([a-zA-Z0-9]+)/SMS/', 'SMS',
        '/cases/([a-zA-Z0-9]+)/UserDictionary/', 'UserDictionary',
        )

render = web.template.render('templates/')

class favicon(object):
    """
    On base web.py process, the request for favicon.ico 404s, this make it
    displayable and thus avoid the 404s.
    """
    def GET(self):
        raise web.redirect('static/favicon.ico')


class CallLog(object):
    def GET(self):
        name = 'Mateen'
        casedir = os.path.join(os.getcwd(), 'cases')
        calllogs = os.path.join(casedir, name, 'Call Log.csv')
        calls = calllog(calllogs)
        return render.calllog(name, calls)

class ShowCase(object):
    def GET(self, name):
        curdir = os.path.join(os.getcwd(), 'cases', name)
        casename = name
        casefiles = ['BrowserHistory',  'BrowserSearches',  'CallLog',  'Contacts',  'Media',  'MMSAttachments',  'MMS',  'SMS',  'UserDictionary']
        cases = []
        caseinfo = ''
        cases_dir = 'cases'
        for dirs in os.walk(cases_dir):
            cases.append(dirs)
        direc = cases[0][1]
        if not name in direc:
            message = "There's no case with the name: %s" % name
            return render.showcase(message, caseinfo)
        else:
            message = ''
            caseinfo = infoxml(os.path.join(curdir, 'info.xml'))
            return render.showcase(message, caseinfo, casename, casefiles)


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
            fout.write(zip_list.read(item))
            fout.close()
        return web.seeother('/')

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
