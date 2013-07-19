#!/usr/bin/env python

import csv
from bs4 import BeautifulSoup
from datetime import datetime

def epoch2datetime(t):
    """Convert milliseconds from epoch to a local datetime object"""
    return datetime.fromtimestamp(t/1000.0)

def infoxml(path):
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
    buildinfo = [verrel, versdk, verinc, board, brand, device, display, fingerprint, host, ident, model, product, tags, timeb, typeand, user]
    return [phoneinfo, buildinfo]

def calllog(path):
    storage = []
    calllogcsv = open(path)
    things = csv.reader(calllogcsv, delimiter=",", quotechar='"')
    column_names = things.next()
    for line in things:
        storage.append(line)
    for row in storage:
        row[2] = epoch2datetime(int(row[2]))
    return [column_names, storage]
