'''
    gdrive (Google Drive ) for KODI / XBMC Plugin
    Copyright (C) 2013-2016 ddurdle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''

import os
import re
import urllib, urllib2
import cookielib

import xbmc, xbmcaddon, xbmcgui, xbmcplugin

import authorization
import crashreport
from resources.lib import package
from resources.lib import file
from resources.lib import folder


class gSpreadsheets:

    S_CHANNEL=0
    S_MONTH=1
    S_DAY=2
    S_WEEKDAY=3
    S_HOUR=4
    S_MINUTE=5
    S_SHOW=6
    S_ORDER=7
    S_INCLUDE_WATCHED=8


    D_SOURCE=0
    D_NFO=1
    D_SHOW=2
    D_SEASON=3
    D_EPISODE=4
    D_PART=5
    D_WATCHED=6
    D_DURATION=7

    def __init__(self, service, addon, user_agent):
        self.addon = addon
        self.service = service
#        self.crashreport = crashreport
#        self.crashreport.sendError('test','test')

        self.user_agent = user_agent

        return



    #
    # returns a list of spreadsheets and a link to their worksheets
    #
    def getSpreadsheetList(self):

        url = 'https://spreadsheets.google.com/feeds/spreadsheets/private/full'

        spreadsheets = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    if e.msg != '':
                        xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), e.msg)
                        xbmc.log(self.addon.getAddonInfo('getSpreadsheetList') + ': ' + str(e), xbmc.LOGERROR)
                        self.crashreport.sendError('getSpreadsheetList',str(e))
              else:
                if e.msg != '':
                    xbmcgui.Dialog().ok(self.addon.getLocalizedString(30000), e.msg)
                    xbmc.log(self.addon.getAddonInfo('getSpreadsheetList') + ': ' + str(e), xbmc.LOGERROR)
                    self.crashreport.sendError('getSpreadsheetList',str(e))

            response_data = response.read()
            response.close()


            for r in re.finditer('<title [^\>]+\>([^<]+)</title><content [^\>]+\>[^<]+</content><link rel=\'[^\#]+\#worksheetsfeed\' type=\'application/atom\+xml\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                title,url = r.groups()

                # must be read/write spreadsheet, skip read-only
                regexp = re.compile(r'/private/values')
                if regexp.search(url) is None:
                    spreadsheets[title] = url

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()


            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return spreadsheets

    #
    # returns a list of spreadsheets contained in the Google Docs account
    #
    def createWorksheet(self,url,title,cols,rows):

        header = { 'User-Agent' : self.user_agent, 'Authorization' : 'GoogleLogin auth=%s' % self.authorization.getToken('wise'), 'GData-Version' : '3.0',  'Content-Type': 'application/atom+xml' }

        entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gs="http://schemas.google.com/spreadsheets/2006"><title>A worksheetdadf</title><gs:rowCount>100</gs:rowCount><gs:colCount>20</gs:colCount></entry>'

        req = urllib2.Request(url, entry, header)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
          if e.code == 403 or e.code == 401:
            self.service.refreshToken()
            req = urllib2.Request(url, None, self.service.getHeadersList())
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return False
          else:
            xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
            return False


        response_data = response.read()
        response.close()

        return True

    #
    # returns a list of spreadsheets contained in the Google Docs account
    #
    def createRow(self,url, folderID, folderName, fileID, fileName):


#        header = { 'User-Agent' : self.user_agent, 'Authorization' : 'GoogleLogin auth=%s' % self.authorization.getToken('wise'), 'GData-Version' : '3.0',  'Content-Type': 'application/atom+xml'}
        header = { 'User-Agent' : self.user_agent, 'Authorization' : 'Bearer ' + self.service.authorization.getToken('auth_access_token'), 'GData-Version' : '3.0',  'Content-Type': 'application/atom+xml'}

        entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"> <gsx:source>S3E12 - The Red Dot.avi-0002</gsx:source><gsx:nfo>test.nfo</gsx:nfo><gsx:show>Seinfeld</gsx:show><gsx:season>3</gsx:season><gsx:episode>1</gsx:episode><gsx:part>1</gsx:part><gsx:watched>0</gsx:watched><gsx:duration>1</gsx:duration></entry>'

        req = urllib2.Request(url, entry, header)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
          if e.code == 403 or e.code == 401:
            self.service.refreshToken()
            req = urllib2.Request(url, None, self.service.getHeadersList())
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return False
          else:
            xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
            return False

        response_data = response.read()
        response.close()

        return True

    #
    # returns a list of spreadsheets contained in the Google Docs account
    #
    def createMediaStatus(self, url, package, resume='', watched='', updated=''):

        import time
        updated = time.strftime("%Y%m%d%H%M")


#        header = { 'User-Agent' : self.user_agent, 'Authorization' : 'GoogleLogin auth=%s' % self.authorization.getToken('wise'), 'GData-Version' : '3.0',  'Content-Type': 'application/atom+xml'}
        header = { 'User-Agent' : self.user_agent, 'Authorization' : 'Bearer ' + self.service.authorization.getToken('auth_access_token'),  'Content-Type': 'application/atom+xml'}

        #entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"> <gsx:folderid>'+str(package.folder.id)+'</gsx:folderid><gsx:foldername>'+str(package.folder.title)+'</gsx:foldername><gsx:fileid>'+str(package.file.id)+'</gsx:fileid><gsx:filename>'+str(package.file.title)+'</gsx:filename><gsx:nfo></gsx:nfo><gsx:order></gsx:order><gsx:watched>'+str(watched)+'</gsx:watched><gsx:resume>'+str(resume)+'</gsx:resume><gsx:updated>'+str(updated)+'</gsx:updated></entry>'
##        entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"><gsx:fileid>'+str(package.file.id)+'</gsx:fileid><gsx:filename>'+str(package.file.title)+'</gsx:filename><gsx:watched>'+str(watched)+'</gsx:watched><gsx:resume>'+str(resume)+'</gsx:resume>'
#        entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gs="http://schemas.google.com/spreadsheets/2006" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"><entry>' + '<gsx:fileid>'+str(package.file.id)+'</gsx:fileid><gsx:filename>'+str(package.file.title)+'</gsx:filename><gsx:watched>'+str(watched)+'</gsx:watched><gsx:resume>'+str(resume)+'</gsx:resume></entry>'
#        entry = '<entry xmlns="http://www.w3.org/2005/Atom"    xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"><entry>' + '<gsx:fileid>'+str(package.file.id)+'</gsx:fileid><gsx:filename>'+str(package.file.title)+'</gsx:filename><gsx:watched>'+str(watched)+'</gsx:watched><gsx:resume>'+str(resume)+'</gsx:resume></entry>'
        entry = '<entry xmlns="http://www.w3.org/2005/Atom"    xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">' + '<gsx:foldername>'+str(package.folder.title)+'</gsx:foldername><gsx:folderid>'+str(package.folder.id)+'</gsx:folderid><gsx:fileid>'+str(package.file.id)+'</gsx:fileid><gsx:filename>'+str(package.file.title)+'</gsx:filename><gsx:watched>'+str(watched)+'</gsx:watched><gsx:md5>'+str(package.file.checksum)+'</gsx:md5><gsx:resume>'+str(resume)+'</gsx:resume><gsx:updated>'+str(updated)+'</gsx:updated></entry>'
        req = urllib2.Request(url, entry, header)
#        req = urllib2.Request(url, entry, self.service.getHeadersList(isPOST=True))

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
          if e.code == 403 or e.code == 401:
            self.service.refreshToken()
            header = { 'User-Agent' : self.user_agent, 'Authorization' : 'Bearer ' + self.service.authorization.getToken('auth_access_token'),  'Content-Type': 'application/atom+xml'}

            req = urllib2.Request(url, entry, header)
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return False
          else:
            xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
            return False

        response_data = response.read()
        response.close()

        return True


    #
    # returns a list of spreadsheets contained in the Google Docs account
    #
    def createHeaderRow(self,url):

        header = { 'User-Agent' : self.user_agent, 'Authorization' : 'GoogleLogin auth=%s' % self.authorization.getToken('wise'), 'GData-Version' : '3.0',  "If-Match" : '*', 'Content-Type': 'application/atom+xml'}

        entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"> <gsx:hours>1</gsx:hours></entry>'

        req = urllib2.Request(url, entry, header)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
          if e.code == 403 or e.code == 401:
            self.service.refreshToken()
            header = { 'User-Agent' : self.user_agent, 'Authorization' : 'GoogleLogin auth=%s' % self.authorization.getToken('wise'), 'GData-Version' : '3.0',  "If-Match" : '*', 'Content-Type': 'application/atom+xml'}
            req = urllib2.Request(url, entry, header)
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return False
          else:
            xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
            return False

        response_data = response.read()
        response.close()

        return True

    #
    # returns a list of worksheets with a link to their listfeeds
    #
    def getSpreadsheetWorksheets(self,url):

        worksheets = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('getSpreadsheetWorksheets') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('getSpreadsheetWorksheets') + ': ' + str(e), xbmc.LOGERROR)

            response_data = response.read()
            response.close()


            for r in re.finditer('<title[^>]+\>([^<]+)</title><content[^>]+\>[^<]+</content><link rel=\'[^\#]+\#listfeed\' type=\'application/atom\+xml\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                title,url = r.groups()
                worksheets[title] = url

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()


            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return worksheets



    #
    # returns a list of worksheets with a link to their listfeeds
    #
    def getSpreadsheetWorksheets(self,url):

        worksheets = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('getSpreadsheetWorksheets') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('getSpreadsheetWorksheets') + ': ' + str(e), xbmc.LOGERROR)

            response_data = response.read()
            response.close()


            for r in re.finditer('<title[^>]+\>([^<]+)</title><content[^>]+\>[^<]+</content><link rel=\'[^\#]+\#listfeed\' type=\'application/atom\+xml\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                title,url = r.groups()
                worksheets[title] = url

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()


            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return worksheets



    #spreadsheet STRM
    def getSTRMplaybackMovie(self,url,title,year):


        params = urllib.urlencode({'title': '"' +str(title)+'"'}, {'year': year})
        url = url + '?sq=' + params


        files = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    return ''
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return ''
            response_data = response.read()

            count=0;
            for r in re.finditer('<gsx:mins>([^<]*)</gsx:mins><gsx:resolution>([^<]*)</gsx:resolution><gsx:md5>[^<]*</gsx:md5><gsx:filename>[^<]*</gsx:filename><gsx:fileid>([^<]*)</gsx:fileid>' ,
                             response_data, re.DOTALL):
                files[count] = r.groups()
#source,nfo,show,season,episode,part,watched,duration
#channel,month,day,weekday,hour,minute,show,order,includeWatched
                count = count + 1

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]

        if len(files) == 0:
            return ''
        elif len(files) == 1:
            return files[0][2]


        options = []

        if files:
            for item in files:
                    options.append('resolution ' + str(files[item][1]) + 'p - mins '  + str(files[item][0]))

        ret = xbmcgui.Dialog().select(self.addon.getLocalizedString(30112), options)
        return files[ret][2]





    def getShows(self,url,channel):


        params = urllib.urlencode({'channel': channel})
        url = url + '?sq=' + params


        shows = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)

            response_data = response.read()

            count=0;
            for r in re.finditer('<gsx:channel>([^<]*)</gsx:channel><gsx:month>([^<]*)</gsx:month><gsx:day>([^<]*)</gsx:day><gsx:weekday>([^<]*)</gsx:weekday><gsx:hour>([^<]*)</gsx:hour><gsx:minute>([^<]*)</gsx:minute><gsx:show>([^<]*)</gsx:show><gsx:order>([^<]*)</gsx:order><gsx:includewatched>([^<]*)</gsx:includewatched>' ,
                             response_data, re.DOTALL):
                shows[count] = r.groups()
#source,nfo,show,season,episode,part,watched,duration
#channel,month,day,weekday,hour,minute,show,order,includeWatched
                count = count + 1

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return shows


    def getMedia(self,url, folderID=None, fileID=None):

        if fileID is None:
            params = urllib.urlencode({'folderid': folderID})
        else:
            params = urllib.urlencode({'fileid': fileID})
        url = url + '?sq=' + params


        media = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)

            response_data = response.read()

            count=0;
#            for r in re.finditer('<gsx:folderid>([^<]*)</gsx:folderid><gsx:foldername>([^<]*)</gsx:foldername><gsx:fileid>([^<]*)</gsx:fileid><gsx:filename>([^<]*)</gsx:filename><gsx:nfo>([^<]*)</gsx:nfo><gsx:order>([^<]*)</gsx:order><gsx:watched>([^<]*)</gsx:watched><gsx:resume>([^<]*)</gsx:resume>' ,
            for r in re.finditer('<gsx:fileid>([^<]*)</gsx:fileid><gsx:filename>([^<]*)</gsx:filename><gsx:watched>([^<]*)</gsx:watched><gsx:resume>([^<]*)</gsx:resume>' ,
                             response_data, re.DOTALL):
                media[count] = r.groups()
                count = count + 1

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return media


    def updateMediaPackage(self,url, package1=None, criteria=''):

        if package1 is not None and (package1.file is None or package1.file.id is None) and package1.folder is not None and package1.folder.id is not None:
            params = urllib.urlencode({'folderid':  package1.folder.id})
        elif package1 is not None and (package1.file is None or package1.file.id is not None) and package1.folder is not None and package1.folder.id is not None and  package1.folder.id != '' :
            params = str(urllib.urlencode({'folderid':  package1.folder.id})) +'%20or%20'+ str(urllib.urlencode({'fileid':  package1.file.id}))
        elif package1 is not None and package1.file is not None and package1.file.id is not None:
            params = urllib.urlencode({'fileid':  package1.file.id})
        elif package1 is None and criteria == 'library':
            params = 'foldername!=""&orderby=column:folderid'
        elif package1 is None and criteria == 'queued':
            params = 'folderid=QUEUED&orderby=column:order'
        elif package1 is None and criteria == 'recentwatched':
            from datetime import date, timedelta
            updated = str((date.today() - timedelta(1)).strftime("%Y%m%d%H%M"))
            params = 'folderid!=QUEUED%20and%20watched!=""%20and%20watched>0%20and%20updated>='+updated
        elif package1 is None and criteria == 'recentstarted':
            from datetime import date, timedelta
            updated = str((date.today() - timedelta(1)).strftime("%Y%m%d%H%M"))
            params = 'folderid!=QUEUED%20and%20watched=""%20and%20resume>0%20and%20updated>='+updated
        else:
            return
        url = url + '?sq=' + params
       #url = url + '?tq=' + params


        mediaList = []
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return

            response_data = response.read()

            previous = ''
            append = True
#            for r in re.finditer('<gsx:folderid>([^<]*)</gsx:folderid><gsx:foldername>([^<]*)</gsx:foldername><gsx:fileid>([^<]*)</gsx:fileid><gsx:filename>([^<]*)</gsx:filename><gsx:nfo>([^<]*)</gsx:nfo><gsx:order>([^<]*)</gsx:order><gsx:watched>([^<]*)</gsx:watched><gsx:resume>([^<]*)</gsx:resume>' ,
            for r in re.finditer('<entry>(.*?)</entry>' ,
                             response_data, re.DOTALL):

                #media = r.groups()
                entry = r.group()
                #exp = re.compile('<gsx:([^\>]+)>(.*)</gsx')
                #exp = re.compile('<gsx:([^\>]+)>([^<]+)</')
                exp = re.compile('<gsx:([^\>]+)>([^<]+)</gsx')
                if package1 is None:
                    newPackage = package.package( file.file('', '', '', self.service.MEDIA_TYPE_VIDEO, '',''),folder.folder('',''))
                else:
                    newPackage = package1


                for media in exp.finditer(entry):
                    # not a general folder ID but another file ID
                    if media.group(1) == 'fileid' and newPackage.file.id != '' and newPackage.file.id != media.group(2) and media.group(2) != '':
                        break
                    elif media.group(1) == 'folderid':
                        newPackage.folder.id = media.group(2)
                    elif media.group(1) == 'foldername':
                        newPackage.folder.title = media.group(2)
                        newPackage.folder.displaytitle = media.group(2)

                        if  criteria == 'library':
                            newPackage.file = None
                            if previous == newPackage.folder.id:
                                append = False
                            else:
                                append = True
                                previous = newPackage.folder.id
                            break

                    elif media.group(1) == 'watched':
                        if  media.group(2) == '':
                            newPackage.file.playcount = 0
                        else:
                            newPackage.file.playcount =  media.group(2)

                    elif media.group(1) == 'resume':
                        if  media.group(2) == '':
                            newPackage.file.resume = 0
                        else:
                            newPackage.file.resume = media.group(2)
                    elif media.group(1) == 'commands':
                        newPackage.file.commands = media.group(2)
                    elif media.group(1) == 'nfo':
                        nfoInfo = media.group(2)
                        nfoInfo = re.sub('&lt;', '<', nfoInfo)
                        nfoInfo = re.sub('/\s?&gt;', '> </>', nfoInfo)
                        nfoInfo = re.sub('&gt;', '>', nfoInfo)
                        nfo = re.compile('<([^\>]+)>([^\<]*)</')
                        for info in nfo.finditer(nfoInfo):
                            if info.group(1) == 'title':
                                newPackage.file.title = info.group(2)
                            elif info.group(1) == 'premiered' or info.group(1) == 'year':
                                newPackage.file.date = info.group(2)
                            elif info.group(1) == 'plot' or info.group(1) == 'description':
                                newPackage.file.plot = info.group(2)
                            elif info.group(1) == 'actors':
                                newPackage.file.cast = info.group(2)
                    elif media.group(1) == 'fanart':
                        newPackage.file.fanart = self.service.API_URL +'files/' + str(media.group(2)) + '?alt=media' + '|' + self.service.getHeadersEncoded()

                    elif media.group(1) == 'fileid':
                        newPackage.file.id = media.group(2)
                    elif media.group(1) == 'filename':
                        newPackage.file.title = media.group(2)

                if append:
                    mediaList.append(newPackage)
            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return mediaList


    def updateMediaPackageList(self,url, folderID, mediaList):

        if folderID is not None and folderID != '':
            params = urllib.urlencode({'folderid':  folderID})
        else:
            return
        url = url + '?sq=' + params
       #url = url + '?tq=' + params

        mediaHash = {}
        if mediaList:
            count=0
            for item in mediaList:
                if item.file is not None:
                    mediaHash[item.file.id] = count
                count = count + 1


        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return

            response_data = response.read()

            previous = ''
            append = True
            for r in re.finditer('<entry>(.*?)</entry>' ,
                             response_data, re.DOTALL):

                entry = r.group()
                exp = re.compile('<gsx:([^\>]+)>([^<]+)</gsx')


                for media in exp.finditer(entry):
                    # not a general folder ID but another file ID
                    if media.group(1) == 'fileid' and media.group(2) not in mediaHash.keys():
                        break
                    elif media.group(1) == 'folderid' and media.group(2) not in mediaHash.keys():
                        break

                    elif media.group(1) == 'fileid':
                        newPackage = mediaList[mediaHash[media.group(2)]]

                    elif media.group(1) == 'watched':
                        if  media.group(2) == '':
                            newPackage.file.playcount = 0
                        else:
                            newPackage.file.playcount =  media.group(2)
                    elif media.group(1) == 'resume':
                        if  media.group(2) == '':
                            newPackage.file.cloudResume = 0
                        else:
                            newPackage.file.cloudResume = media.group(2)
                    elif media.group(1) == 'commands':
                        newPackage.file.commands = media.group(2)
                    elif media.group(1) == 'nfo':
                        nfoInfo = media.group(2)
                        nfoInfo = re.sub('&lt;', '<', nfoInfo)
                        nfoInfo = re.sub('/\s?&gt;', '> </>', nfoInfo)
                        nfoInfo = re.sub('&gt;', '>', nfoInfo)
                        nfo = re.compile('<([^\>]+)>([^\<]*)</')
                        for info in nfo.finditer(nfoInfo):
                            #if info.group(1) == 'title':
                            #    newPackage.file.title = info.group(2)
                            if info.group(1) == 'premiered' or info.group(1) == 'year':
                                newPackage.file.date = info.group(2)
                            elif info.group(1) == 'plot' or info.group(1) == 'description':
                                newPackage.file.plot = info.group(2)
                            elif info.group(1) == 'actors':
                                newPackage.file.cast = info.group(2)
                    elif media.group(1) == 'fanart':
                        newPackage.file.fanart = self.service.API_URL +'files/' + str(media.group(2)) + '?alt=media' + '|' + self.service.getHeadersEncoded()
                    elif media.group(1) == 'filename':
                        newPackage.file.title = media.group(2)

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return mediaList

    ## not in use
    def getMediaPackageList(self,url, folderName, mediaList):

        if folderName is not None and folderName != '':
            params = urllib.urlencode({'foldername':  folderName, 'folderid': ''})
        else:
            return
        url = url + '?sq=' + params
       #url = url + '?tq=' + params

        mediaHash = {}
        if mediaList:
            count=0
            for item in mediaList:
                if item.file is not None:
                    mediaHash[item.file.id] = count
                count = count + 1


        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return

            response_data = response.read()

            previous = ''
            append = True
            for r in re.finditer('<entry>(.*?)</entry>' ,
                             response_data, re.DOTALL):

                entry = r.group()
                exp = re.compile('<gsx:([^\>]+)>([^<]+)</gsx')


                for media in exp.finditer(entry):
                    # not a general folder ID but another file ID
                    if media.group(1) == 'fileid' and media.group(2) not in mediaHash.keys():
                        break
                    elif media.group(1) == 'fileid':
                        newPackage = mediaList[mediaHash[media.group(2)]]

                    elif media.group(1) == 'watched':
                        if  media.group(2) == '':
                            newPackage.file.playcount = 0
                        else:
                            newPackage.file.playcount =  media.group(2)
                    elif media.group(1) == 'resume':
                        if  media.group(2) == '':
                            newPackage.file.cloudResume = 0
                        else:
                            newPackage.file.cloudResume = media.group(2)
                    elif media.group(1) == 'commands':
                        newPackage.file.commands = media.group(2)
                    elif media.group(1) == 'nfo':
                        nfoInfo = media.group(2)
                        nfoInfo = re.sub('&lt;', '<', nfoInfo)
                        nfoInfo = re.sub('/\s?&gt;', '> </>', nfoInfo)
                        nfoInfo = re.sub('&gt;', '>', nfoInfo)
                        nfo = re.compile('<([^\>]+)>([^\<]*)</')
                        for info in nfo.finditer(nfoInfo):
                            if info.group(1) == 'title':
                                newPackage.file.title = info.group(2)
                            elif info.group(1) == 'premiered' or info.group(1) == 'year':
                                newPackage.file.date = info.group(2)
                            elif info.group(1) == 'plot' or info.group(1) == 'description':
                                newPackage.file.plot = info.group(2)
                            elif info.group(1) == 'actors':
                                newPackage.file.cast = info.group(2)
                    elif media.group(1) == 'fanart':
                        newPackage.file.fanart = self.service.API_URL +'files/' + str(media.group(2)) + '?alt=media' + '|' + self.service.getHeadersEncoded()
                    elif media.group(1) == 'filename':
                        newPackage.file.title = media.group(2)

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return mediaList


    def getMediaInformation(self,url,folderID):

        params = urllib.urlencode({'folderuid': folderID})
        url = url + '?sq=' + params


        media = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                    return
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
                return

            response_data = response.read()

            count=0;
            for r in re.finditer('<gsx:foldername>([^<]*)</gsx:foldername><gsx:folderuid>([^<]*)</gsx:folderuid><gsx:filename>([^<]*)</gsx:filename><gsx:fileuid>([^<]*)</gsx:fileuid><gsx:season>([^<]*)</gsx:season><gsx:episode>([^<]*)</gsx:episode><gsx:watched>([^<]*)</gsx:watched><gsx:sequence>([^<]*)</gsx:sequence>' ,
                             response_data, re.DOTALL):
                media[count] = r.groups()
                count = count + 1

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]


        return media

    def getVideo(self,url,show):
        params = urllib.urlencode({'show': show})
        url = url + '?sq=' + params + '+and+watched=0'


        shows = {}
        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)

            response_data = response.read()

            count=0;
            for r in re.finditer('<entry[^\>]*>.*?<gsx:source>([^<]*)</gsx:source><gsx:nfo>([^<]*)</gsx:nfo><gsx:show>([^<]*)</gsx:show><gsx:season>([^<]*)</gsx:season><gsx:episode>([^<]*)</gsx:episode><gsx:part>([^<]*)</gsx:part><gsx:watched>([^<]*)</gsx:watched><gsx:duration>([^<]*)</gsx:duration></entry>' ,
                             response_data, re.DOTALL):
                shows[count] = r.groups()
                #source,nfo,show,season,episode,part,watched,duration
                count = count + 1

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:

                url = nextURL[0]

        return shows


    def setVideoWatched(self,url,source):

#        import urllib
#        from cookielib import CookieJar

#        cj = CookieJar()
#        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#        urllib2.install_opener(opener)


        source = re.sub(' ', '+', source)
#        params = urllib.urlencode(source)
        url = url + '?sq=source="' + source +'"'

        req = urllib2.Request(url, None, self.service.getHeadersList())

        try:
            response = urllib2.urlopen(req)
#            response = opener.open(url, None,urllib.urlencode(header))
        except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)

        response_data = response.read()
        response.close()

        editURL=''
        for r in re.finditer('<link rel=\'(edit)\' type=\'application/atom\+xml\' href=\'([^\']+)\'/>' ,
                             response_data, re.DOTALL):
            (x,editURL) = r.groups(1)

        for r in re.finditer('<link rel=\'edit\' [^\>]+>(.*?</entry>)' ,
                             response_data, re.DOTALL):
            entry = r.group(1)

        entry = re.sub('<gsx:watched>([^\<]*)</gsx:watched>', '<gsx:watched>1</gsx:watched>', entry)


#        entry = re.sub(' gd\:etag[^\>]+>', ' xmlns="http://www.w3.org/2005/Atom" xmlns:gs="http://schemas.google.com/spreadsheets/2006" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">', entry)
#        entry = re.sub('<entry>', '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">', entry)
        #entry = re.sub('<entry>', '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended"> ', entry)
        entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gs="http://schemas.google.com/spreadsheets/2006" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">' + entry
#        entry  = "<?xml version='1.0' encoding='UTF-8'?><entry xmlns='http://www.w3.org/2005/Atom' xmlns:gsx='http://schemas.google.com/spreadsheets/2006/extended'><id>https://spreadsheets.google.com/feeds/list/147ajW3jRGUTwcuBSLx5dYw5ar17fo9NPtu8azHa3j0w/od6/private/full/1lcxsw</id><updated>2015-05-01T18:49:50.299Z</updated><category scheme='http://schemas.google.com/spreadsheets/2006' term='http://schemas.google.com/spreadsheets/2006#list'/><title type='text'>S3E12 - The Red Dot.avi-0002</title><content type='text'>nfo: test.nfo, show: Seinfeld, season: 3, episode: 1, part: 1, watched: 0, duration: 1</content><link rel='self' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/list/147ajW3jRGUTwcuBSLx5dYw5ar17fo9NPtu8azHa3j0w/od6/private/full/1lcxsw'/><link rel='edit' type='application/atom+xml' href='https://spreadsheets.google.com/feeds/list/147ajW3jRGUTwcuBSLx5dYw5ar17fo9NPtu8azHa3j0w/od6/private/full/1lcxsw/in881g9gmnffm'/><gsx:source>S3E12 - The Red Dot.avi-0002</gsx:source><gsx:nfo>test.nfo</gsx:nfo><gsx:show>Seinfeld</gsx:show><gsx:season>3</gsx:season><gsx:episode>1</gsx:episode><gsx:part>1</gsx:part><gsx:watched>0</gsx:watched><gsx:duration>1</gsx:duration></entry>"
#xmlns:gsx='http://schemas.google.com/spreadsheets/2006/extended'
#        entry = " <?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:gsx='http://schemas.google.com/spreadsheets/2006/extended' xmlns:gd=\"http://schemas.google.com/g/2005\">"+entry
#        entry = '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:openSearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended" xmlns:gd="http://schemas.google.com/g/2005" gd:etag=\'W/"D0cERnk-eip7ImA9WBBXGEg."\'><entry>  <id>    https://spreadsheets.google.com/feeds/worksheets/key/private/full/worksheetId  </id>  <updated>2007-07-30T18:51:30.666Z</updated>  <category scheme="http://schemas.google.com/spreadsheets/2006"    term="http://schemas.google.com/spreadsheets/2006#worksheet"/>  <title type="text">Income</title>  <content type="text">Expenses</content>  <link rel="http://schemas.google.com/spreadsheets/2006#listfeed"    type="application/atom+xml" href="https://spreadsheets.google.com/feeds/list/key/worksheetId/private/full"/>  <link rel="http://schemas.google.com/spreadsheets/2006#cellsfeed"    type="application/atom+xml" href="https://spreadsheets.google.com/feeds/cells/key/worksheetId/private/full"/>  <link rel="self" type="application/atom+xml"    href="https://spreadsheets.google.com/feeds/worksheets/key/private/full/worksheetId"/>  <link rel="edit" type="application/atom+xml"    href="https://spreadsheets.google.com/feeds/worksheets/key/private/full/worksheetId/version"/>  <gs:rowCount>45</gs:rowCount>  <gs:colCount>15</gs:colCount></entry>'

#        req = urllib2.Request(editURL, entry, header)
#        urllib2.HTTPHandler(debuglevel=1)
#        req.get_method = lambda: 'PUT'

        req = urllib2.Request(editURL, entry, self.service.getHeadersList(isPOST=True))
        req.get_method = lambda: 'PUT'

#        req.get_method = lambda: 'DELETE'



        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
          if e.code == 403 or e.code == 401:
            self.service.refreshToken()
            req = urllib2.Request(url, None, self.service.getHeadersList())
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e.read()), xbmc.LOGERROR)
          else:
            xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e.read()), xbmc.LOGERROR)


        response_data = response.read()

        response.close()




    def setMediaStatus(self, url, package, resume='', watched=''):


        import time
        updated = time.strftime("%Y%m%d%H%M")

        newurl = url + '?sq=fileid="' + str(package.file.id) +'"'

        req = urllib2.Request(newurl, None, self.service.getHeadersList())

        try:
            response = urllib2.urlopen(req)
#            response = opener.open(url, None,urllib.urlencode(header))
        except urllib2.URLError, e:
          if e.code == 403 or e.code == 401:
            self.service.refreshToken()
            req = urllib2.Request(url, None, self.service.getHeadersList())
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
          else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)


        response_data = response.read()
        response.close()

        editURL=''
        for r in re.finditer('<link rel=\'edit\' type=\'application/atom\+xml\' href=\'([^\']+)\'/>' ,
                             response_data, re.DOTALL):
            editURL = r.group(1)

        for r in re.finditer('<link rel=\'edit\' [^\>]+>(.*?</entry>)' ,
                             response_data, re.DOTALL):
            entry = r.group(1)


        if editURL != '':

            if resume != '':
                entry = re.sub('<gsx:resume>([^\<]*)</gsx:resume>', '<gsx:resume>'+str(resume)+'</gsx:resume>', entry)

            if watched != '':
                entry = re.sub('<gsx:watched>([^\<]*)</gsx:watched>', '<gsx:watched>'+str(watched)+'</gsx:watched>', entry)

            entry = re.sub('<gsx:updated>([^\<]*)</gsx:updated>', '<gsx:updated>'+str(updated)+'</gsx:updated>', entry)


            entry = '<?xml version=\'1.0\' encoding=\'UTF-8\'?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:gs="http://schemas.google.com/spreadsheets/2006" xmlns:gsx="http://schemas.google.com/spreadsheets/2006/extended">' + entry

            req = urllib2.Request(editURL, entry, self.service.getHeadersList(isPOST=True))
            req.get_method = lambda: 'PUT'

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e.read()), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e.read()), xbmc.LOGERROR)


            response_data = response.read()
            response.close()
        else:
            if resume != '' and watched != '':
                self.createMediaStatus(url,package,resume,watched, updated=updated)
            elif resume != '' and watched == '':
                self.createMediaStatus(url,package,resume=resume, updated=updated)
            elif resume == '' and watched != '':
                self.createMediaStatus(url,package,watched=watched, updated=updated)
            else:
                self.createMediaStatus(url,package, updated=updated)


    def getChannels(self,url):
        params = urllib.urlencode({'orderby': 'channel'})
        url = url + '?' + params


        channels = []
        count=0

        while True:
            req = urllib2.Request(url, None, self.service.getHeadersList())

            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
              if e.code == 403 or e.code == 401:
                self.service.refreshToken()
                req = urllib2.Request(url, None, self.service.getHeadersList())
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)
              else:
                xbmc.log(self.addon.getAddonInfo('name') + ': ' + str(e), xbmc.LOGERROR)


            response_data = response.read()


            for r in re.finditer('<gsx:channel>([^<]*)</gsx:channel>' ,
                             response_data, re.DOTALL):
                (channel) = r.groups()
                #channel,month,day,weekday,hour,minute,show,order,includeWatched
                if not channels.__contains__(channel[0]):
                  channels.append(channel[0])
                  count = count + 1

            nextURL = ''
            for r in re.finditer('<link rel=\'next\' type=\'[^\']+\' href=\'([^\']+)\'' ,
                             response_data, re.DOTALL):
                nextURL = r.groups()

            response.close()

            if nextURL == '':
                break
            else:
                url = nextURL[0]

        return channels


