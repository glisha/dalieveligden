# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from skopjetz import EuropeSkopje
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

sktz = EuropeSkopje()

class MainPage(webapp.RequestHandler):
    global veligden_datumi
    global katolicki_datumi

    def get(self):
        if self.request.path.startswith('/katolicki'):
            datumi = katolicki_datumi
        else:
            datumi = veligden_datumi

        sega = datetime.datetime.now(sktz)
        deneska = datetime.datetime(sega.year,sega.month,sega.day,0,0)

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

        sega = datetime.datetime.now(sktz)
        deneska = datetime.datetime(sega.year,sega.month,sega.day,0,0)

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
    global katolicki_datumi

    def get(self):
        sega = datetime.datetime.now(sktz)
        deneska = datetime.datetime(sega.year,sega.month,sega.day,0,0)

        if self.request.path.startswith('/katolicki'):
            datumiv = katolicki_datumi
        else:
            datumiv = veligden_datumi

        a = [x for x in datumiv]
        a.reverse()
        for redenbroj,veligden in enumerate(a):
            if deneska > veligden:
                sledenveligden = a[redenbroj-1]
                break
            else:
                sledenveligden = a[-1]

        sledenveligdenjs = sledenveligden.strftime('%m/%d/%Y %H:%M AM UTC+0200')
        self.response.out.write(template.render('ushtekolku.template',
                                                    {'sledenveligden':sledenveligdenjs,
                                                    'denovi':(sledenveligden-deneska).days}))

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/katolicki/',MainPage),
                                      ('/rss.xml',RssPage),
                                      ('/katolicki/rss.xml',RssPage),
                                      ('/ushtekolku',UshteKolkuPage),
                                        ('/katolicki/ushtekolku',UshteKolkuPage),
                                        ],
                                     debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
