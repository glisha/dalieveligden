import datetime

class EuropeSkopje(datetime.tzinfo):
    """TZ info za Makedonija
    
        Letno smetanje na vremeto e od Poslednata nedela 
        vo mart do poslednata nedela vo oktomvri.
        http://en.wikipedia.org/wiki/European_Summer_Time#Exact_timing_in_the_next_several_years
        
        Datumot vo mart se presmetuva so:
            (31 - (5y / 4 + 4) mod 7)

        Datumot vo Oktomvri se presemtuva so:
            (31 - (5y / 4 + 1) mod 7)

        Ako deneska e izmegju Mart i Oktomvri vremeto e CEST (UTC+1),
        ako e izmegju Oktomvri i Mart togash e CET (UTC+2)
    """

    def __repr__(self):
        return 'Europe/Skopje'

    def tzname(self, dt):
        if self.dst(dt):
            return 'CET'
        else:
            return 'CEST'

    def utcoffset(self, dt):
        return datetime.timedelta(hours=1) + self.dst(dt)

    def dst(self,dt):
        if dt is None or dt.tzinfo is None:
            return datetime.timedelta(0)
        
        #poslednata nedela vo mart i oktomvri
        pocetokletno = datetime.datetime(dt.year,3,31-(5*dt.year/4+4)%7,2)
        krajletno = datetime.datetime(dt.year,10,31-(5*dt.year/4 + 1)%7,3)
   
        #megju mart i oktomvri e letno smetanje t.e. UTC+1
        if pocetokletno <= dt.replace(tzinfo=None) < krajletno:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

#skopjetz = EuropeSkopje()
#print datetime.datetime.now(skopjetz)
