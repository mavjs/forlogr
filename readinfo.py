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

import csv
from bs4 import BeautifulSoup
from datetime import datetime

def epoch2datetime(t):
    """
    Convert milliseconds from epoch to a local datetime object.
    """
    return datetime.fromtimestamp(t/1000.0)

def epoch2local(t):
    """
    Convert seconds from epoch to a local datetime object.
    """
    return datetime.fromtimestamp(t)

def infoxml(path):
    """
    Get necessary data from info.xml for ShowCase view class.
    Especially the IMEI and build info.
    """
    xmlfile = open(path).read()
    phoneinfo = []
    buildinfo = []
    soup = BeautifulSoup(xmlfile, 'xml')
    tstp = soup.find('date-time').text
    imsi = soup.find('IMSI').text
    imei = soup.find('IMEI-MEID').text
    phonetype = soup.find('phone-type').text
    msisdn = soup.find('MSISDN-MDN').text
    iccid = soup.find('ICCID').text
    build = soup.find('build')
    verrel = build.find('version.release').text
    versdk = build.find('version.sdk').text
    verinc = build.find('version.incremental').text
    board = build.find('board').text
    brand = build.find('brand').text
    device = build.find('device').text
    display = build.find('display').text
    fingerprint = build.find('fingerprint').text
    host = build.find('host').text
    ident = build.find('id').text
    model = build.find('model').text
    product = build.find('product').text
    tags = build.find('tags').text
    timeb = build.find('time').text
    typeand = build.find('type').text
    user = build.find('user').text
    phoneinfo = [tstp, imsi, imei, phonetype, msisdn, iccid]
    buildinfo = [verrel, versdk, verinc, board, brand, device, display,
            fingerprint, host, ident, model, product, tags, timeb, typeand,
            user]
    return [phoneinfo, buildinfo]

def calllog(path):
    """
    Function to parse the Call Log.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    calllogcsv = open(path)
    things = csv.reader(calllogcsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = column_names[1:7]
    for line in things:
        storage.append(line[1:7])
    for row in storage:
        if row[-1] == '':
            row[-1] = 'Unknown'
        row[1] = epoch2datetime(int(row[1]))
    return [column_names, storage]

def browserhistory(path):
    """
    Function to parse the Browser History.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    bhistorycsv = open(path)
    things = csv.reader(bhistorycsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = column_names[1:]
    for line in things:
        storage.append(line[1:])
    for row in storage:
        if row[0] == '':
            row[0] = 'Bookmark'
            continue
        row[0] = epoch2datetime(int(row[0]))
    return [column_names, storage]

def browsersearches(path):
    """
    Function to parse the Browser Searches.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    bsearchcsv = open(path)
    things = csv.reader(bsearchcsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = column_names[1:]
    for line in things:
        storage.append(line[1:])
    for row in storage:
        row[0] = epoch2datetime(int(row[0]))
    return [column_names, storage]

def contacts(path):
    """
    Function to parse the Contacts.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    contactscsv = open(path)
    things = csv.reader(contactscsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = column_names[1:]
    for line in things:
        storage.append(line[1:])
    return [column_names, storage]

def mmsattachments(path):
    """
    Function to parse the MMS Attachments.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    mmsattcsv = open(path)
    things = csv.reader(mmsattcsv, delimiter=",", quotechar='"')
    columns = things.next()
    column_names = [columns[3], columns[4], columns[7], columns[8], columns[9], columns[12], columns[13]]
    for line in things:
        if line[3] == '':
            line[3] = 'N/A'
        if line[4] == '':
            line[4] = 'N/A'
        if line[7] == '':
            line[7] = 'N/A'
        if line[8] == '':
            line[8] = 'N/A'
        if line[9] == '':
            line[9] = 'N/A'
        if line[12] == '':
            line[12] = 'N/A'
        if line[13] == '':
            line[13] = 'N/A'
        storage.append([line[3], line[4], line[7], line[8], line[9], line[12], line[13]])
    return [column_names, storage]

def mms(path):
    """
    Function to parse the MMS.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    contactscsv = open(path)
    things = csv.reader(contactscsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = [column_names[2], column_names[4], column_names[5], column_names[6], column_names[8], column_names[11], column_names[31]]
    for line in things:
        if not line[2] == '':
            line[2] = epoch2local(int(line[2]))
        elif not line[31] == '':
            line[31] = epoch2local(int(line[31]))
        if line[5] == '':
            line[5] = 'N/A'
        if line[6] == '':
            line[6] = 'N/A'
        if line[8] == '':
            line[8] = 'N/A'
        if line[11] == '':
            line[11] = 'N/A'
        storage.append([line[2], line[4], line[5], line[6], line[8], line[11], line[31]])
    return [column_names, storage]

def sms(path):
    """
    Function to parse the SMS.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    smsscsv = open(path)
    things = csv.reader(smsscsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = [column_names[2], column_names[4], column_names[6], column_names[8], column_names[11]]
    for line in things:
        line[4] = epoch2datetime(int(line[4]))
        storage.append([line[2], line[4], line[6], line[8], line[11]])
    return [column_names, storage]

def userdict(path):
    """
    Function to parse the User Dictionary.csv file and strip out unnecessary columns 
    for clarity of report and convert epoch unix times from milliseconds or 
    seconds to proper datetime formats.
    """
    storage = []
    userdictcsv = open(path)
    things = csv.reader(userdictcsv, delimiter=",", quotechar='"')
    column_names = things.next()
    column_names = column_names[1:]
    for line in things:
        storage.append(line[1:])
    return [column_names, storage]
