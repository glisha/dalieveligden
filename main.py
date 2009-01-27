# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import datetime

veligden_datumi = [datetime.datetime(2009,4,19),datetime.datetime(2010,4,4),
                    datetime.datetime(2011,4,24),datetime.datetime(2012,4,15),
                    datetime.datetime(2013,5,5),datetime.datetime(2014,4,20),
                    datetime.datetime(2015,4,12),datetime.datetime(2016,5,1),
                    datetime.datetime(2017,4,16),datetime.datetime(2018,4,8),
                    datetime.datetime(2019,4,28),datetime.datetime(2020,4,19)]

katolicki_datumi = [datetime.datetime(2009,4,12),datetime.datetime(2010,4,4),
                    datetime.datetime(2011,4,24),datetime.datetime(2012,4,8),
                    datetime.datetime(2013,3,31),datetime.datetime(2014,4,20),
                    datetime.datetime(2015,4,5),datetime.datetime(2016,3,27),
                    datetime.datetime(2017,4,16),datetime.datetime(2018,4,1),
                    datetime.datetime(2019,4,21),datetime.datetime(2020,4,12)]

pochetok = datetime.datetime(2008,9,14)

class MainPage(webapp.RequestHandler):
    global veligden_datumi
    global katolicki_datumi

    def get(self):
        if self.request.path.startswith('/katolicki'):
            datumi = katolicki_datumi
        else:
            datumi = veligden_datumi

        deneska = datetime.datetime.strptime(
                        datetime.datetime.now().strftime('%d.%m.%Y 00:00:00'),
                        '%d.%m.%Y 00:00:00')

        dalie = u'НЕ' # ne e sekoj den veligden
        if deneska in datumi:
            dalie = u'ДA, Велигден е!'

        self.response.out.write(template.render('veligden.template', {'dalie':dalie}))

class RssPage(webapp.RequestHandler):
    global veligden_datumi
    global katolicki_datumi

    def get(self):

        if self.request.path.startswith('/katolicki'):
            datumiv = katolicki_datumi
        else:
            datumiv = veligden_datumi


        deneska = datetime.datetime.strptime(
                                datetime.datetime.now().strftime('%d.%m.%Y 00:00:00'),
                                '%d.%m.%Y 00:00:00')
        datumi = []
        for i in range(0,10):
            datum = deneska-datetime.timedelta(i)

            dalie=u'НЕ'
            if datum in datumiv:
                dalie=u'ДА, Велигден е!'

            unikaten = pochetok - datum # da bide unikatno url-to vo rss
            datumi.append((datum,dalie,unikaten.days))

        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(template.render('rss.template',{'datumi':datumi}))

class UshteKolkuPage(webapp.RequestHandler):
    global veligden_datumi

    def get(self):
        deneska = datetime.datetime.now()
        a = [x for x in veligden_datumi]
        a.reverse()
        for redenbroj,veligden in enumerate(a):
            if deneska > veligden:
                sledenveligden = a[redenbroj-1]
                break
            else:
                sledenveligden = a[-1]

        sledenveligdenjs = sledenveligden.strftime('%m/%d/%Y %H:%M AM UTC+0100')
        self.response.out.write(template.render('ushtekolku.template',
                                                    {'sledenveligden':sledenveligdenjs,
                                                    'denovi':(sledenveligden-deneska).days}))

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/katolicki/',MainPage),
                                      ('/rss.xml',RssPage),
                                      ('/katolicki/rss.xml',RssPage),
                                      ('/ushtekolku',UshteKolkuPage),
                                        ],
                                     debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
