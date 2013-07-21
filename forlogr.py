#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Copyright (C) 2012 Maverick JS <mavjs01@gmail.com>, 
# Beard-0 <Beard-0@outlook.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

# import necessary libraries
import os
import web
from StringIO import StringIO
import zipfile

# import the functions defined in readinfo.py
from readinfo import (
        infoxml,
        calllog,
        browserhistory,
        browsersearches,
        contacts,
        mmsattachments,
        mms,
        sms,
        userdict,
        )

# url handling
urls = (
        '/', 'Index',
        '/favicon.ico', 'favicon',
        '/cases', 'Cases',
        '/cases/([a-zA-Z0-9]+)', 'ShowCase',
        '/cases/BrowserHistory/([a-zA-Z0-9]+)', 'BrowserHistory',
        '/cases/BrowserSearches/([a-zA-Z0-9]+)', 'BrowserSearches',
        '/cases/CallLog/([a-zA-Z0-9]+)', 'CallLog',
        '/cases/Contacts/([a-zA-Z0-9]+)', 'Contacts',
        '/cases/MMSAttachments/([a-zA-Z0-9]+)', 'MMSAttachments',
        '/cases/MMS/([a-zA-Z0-9]+)', 'MMS',
        '/cases/SMS/([a-zA-Z0-9]+)', 'SMS',
        '/cases/UserDictionary/([a-zA-Z0-9]+)', 'UserDictionary',
        )

# templates directory
render = web.template.render('templates/')


class favicon(object):
    """
    On base web.py process, the request for favicon.ico 404s, this make it
    displayable and thus avoid the 404s.
    """
    def GET(self):
        raise web.redirect('static/favicon.ico')


class Index(object):
    """
    Class to render the index a.k.a root ('/') of web server, and case name and
    upload view for the web app.
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
        return web.seeother('/cases/%s'  % (casename))


class Cases(object):
    """
    Show the available cases that the investigator has uploaded or just return
    the view if there's none uploaded.
    """
    def GET(self):
        cases = []
        cases_dir = 'cases'
        for dirs in os.walk(cases_dir):
            cases.append(dirs)
        direc = cases[0][1]
        return render.cases(direc)


class ShowCase(object):
    """
    Show the information of the phone associated to a particular case.
    """
    def GET(self, name):
        curdir = os.path.join(os.getcwd(), 'cases', name)
        casename = name
        casefiles = ['BrowserHistory',  'BrowserSearches',  'CallLog',
                'Contacts',  'MMSAttachments',  'MMS',  'SMS',
                'UserDictionary']
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


class BrowserSearches(object):
    """
    Show the informations from Browser Searches.csv file associated to each
    case name.

    e.g. /cases/BrowserSearches/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        bsearches = os.path.join(casedir, name, 'Browser Searches.csv')
        browser = browsersearches(bsearches)
        return render.browsersearches(name, browser)


class BrowserHistory(object):
    """
    Show the informations from Browser History.csv file associated to each
    case name.

    e.g. /cases/BrowserHistory/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        bhistory = os.path.join(casedir, name, 'Browser History.csv')
        browser = browserhistory(bhistory)
        return render.browserhistory(name, browser)


class CallLog(object):
    """
    Show the informations from CallLog.csv file associated to each
    case name.

    e.g. /cases/CallLog/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        calllogs = os.path.join(casedir, name, 'Call Log.csv')
        calls = calllog(calllogs)
        return render.calllog(name, calls)


class Contacts(object):
    """
    Show the informations from Contacts.csv file associated to each
    case name.

    e.g. /cases/Contacts/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        contactscsv = os.path.join(casedir, name, 'Contacts.csv')
        contact = contacts(contactscsv)
        return render.contacts(name, contact)


class MMSAttachments(object):
    """
    Show the informations from MMS Attachments.csv file associated to each
    case name.

    e.g. /cases/MMSAttachments/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        mmsattachcsv = os.path.join(casedir, name, 'MMS Attachments.csv')
        mmsattach = mmsattachments(mmsattachcsv)
        return render.mmsattachments(name, mmsattach)


class MMS(object):
    """
    Show the informations from MMS.csv file associated to each
    case name.

    e.g. /cases/MMS/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        mmscsv = os.path.join(casedir, name, 'MMS.csv')
        mmsA = mms(mmscsv)
        return render.mms(name, mmsA)


class SMS(object):
    """
    Show the informations from SMS.csv file associated to each
    case name.

    e.g. /cases/SMS/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        smscsv = os.path.join(casedir, name, 'SMS.csv')
        smsA = sms(smscsv)
        return render.sms(name, smsA)


class UserDictionary(object):
    """
    Show the informations from User Dictionary.csv file associated to each
    case name.

    e.g. /cases/UserDictionary/Test
    """
    def GET(self, name):
        casedir = os.path.join(os.getcwd(), 'cases')
        userdictcsv = os.path.join(casedir, name, 'User Dictionary.csv')
        userdic = userdict(userdictcsv)
        return render.userdictionary(name, userdic)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
