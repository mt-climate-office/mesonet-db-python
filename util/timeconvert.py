'''
@created="May 2018"
@description=('This class provides the properties and',
              'functions to process time conversions for use'
              'by the Montana Climate Office')
@attention='http://climate.umt.edu
@author: 'Michael D. Sweet',
@email='michael.sweet@umontana.edu',
@organization: 'Montana Climate Office'
#==========================================================================
# USE
#==========================================================================
This class is instantiated to provide resource variables and methods
for managing valid time conversions for Zentra and Mesonet dataa
'''
import datetime
import time
import pytz

LOCAL_TIME_ZONE = pytz.timezone("America/Denver")
#==========================================================================
# Class Definition
#==========================================================================
class MesonetTimeConvert():
    
    """
        Functions and modules for Mesonet\Zentra time conversions
        
        Load using:
            import util.timeconvert
    """

    #==========================================================================
    # Methods for object instantiation
    #==========================================================================
    def __init__(self):
        """
            Initializes properties all time conversions objects
            INPUT:
            PROPERTIES:
            
        """
    
    def if_record_dt_sameday(self,input_dt,record_dt):
        compare = False
        naive_time_dt = datetime.datetime.strptime(input_dt, "%Y-%m-%d %H:%M")
        # print type(naive_time_dt)
        # print type(record_dt)
        inday = datetime.datetime(year=naive_time_dt.year,month=naive_time_dt.month,day=naive_time_dt.day)
        recday = datetime.datetime(year=record_dt.year,month=record_dt.month,day=record_dt.day)
        if inday == recday:
            compare = True
        # print compare
        return compare

    def daterange(self,d1,d2):
        return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))
    
    def datestr_to_naive_dt(self,input_dt):
        naive_time_dt = datetime.datetime.strptime(input_dt, "%Y-%m-%d %H:%M:%S.%f")
        # print "Naive time (no alteration) is: ", naive_time
        return naive_time_dt
    
    def naive_dt_to_local_timestr(self,naive_time_dt):
        local_timestr = LOCAL_TIME_ZONE.localize(naive_time_dt, is_dst=None)
        # print "Local equivalent is: ", local_time
        return local_timestr
    
    def local_timestr_to_UTCstr(self,local_time):
        utc_time_str = local_time.astimezone(pytz.utc)
        # print "UTC equivalent is: ", utc_time
        return utc_time_str
    
    def naive_dt_to_utcms(self,naive_time_dt):
        utc_ms = int(time.mktime(naive_time_dt.utctimetuple()))
        # print "UTC in milliseconds: ", utc_ms
        return utc_ms
    
    def utcms_to_datestr(self,utc_ms):
        datetuple = datetime.datetime.utcfromtimestamp(utc_ms)
        datestr = datetuple.strftime('%Y-%m-%dT%H:%M:%SZ')
        return datestr

    def UTCms_to_localstring(self,utcms):
        datetuple = datetime.datetime.utcfromtimestamp(utcms)
        local_dt = datetuple.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIME_ZONE)
        local_dtn = LOCAL_TIME_ZONE.normalize(local_dt) # .normalize might be unnecessary
        datestr = local_dtn.strftime('%Y-%m-%d %H:%M')
        return datestr

#==========================================================================
# Main and tests
#==========================================================================
if __name__ == "__main__":
    input_dt = "2018-05-04 00:00:00.0"
    print "Input datetime is: ", input_dt
    
    timeconv = MesonetTimeConvert()
    
    # naive_time = datetime.datetime.strptime(input_dt, "%Y-%m-%d %H:%M:%S.%f")
    # print "Naive time (no alteration) is: ", naive_time
    naive_time = timeconv.datestr_to_naive_dt(input_dt)
    print "Naive time (no alteration) is: ", timeconv.datestr_to_naive_dt(input_dt)
    
    # local_time = LOCAL_TIME_ZONE.localize(naive_time, is_dst=None)
    # print "Local equivalent is: ", local_time
    local_time = timeconv.naive_dt_to_local_timestr(naive_time)
    print "Local equivalent is: ", local_time
    
    # utc_time = local_time.astimezone(pytz.utc)
    # print "UTC equivalent is: ", utc_time
    utc_time = timeconv.local_timestr_to_UTCstr(local_time)
    print "UTC equivalent is: ", utc_time
    
    # utc_ms = int(time.mktime(naive_time.utctimetuple()))
    # print "UTC in milliseconds: ", utc_ms
    utc_ms = timeconv.naive_dt_to_utcms(naive_time)
    print "UTC in milliseconds: ", utc_ms
    
    # datetuple = datetime.datetime.utcfromtimestamp(utc_ms)
    # datestr = datetuple.strftime('%Y-%m-%dT%H:%M:%SZ')
    # print "UTC milliseconds to date string: ", datestr
    datestr = timeconv.utcms_to_datestr(1525244400)
    print "UTC milliseconds to date string: ", datestr
    
    print timeconv.UTCms_to_localstring(1525244400)
    """
    print calendar.timegm(time.strptime('Jul 9, 2009 @ 20:02:58 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    print calendar.timegm(time.gmtime())
    print time.time()
    print calendar.timegm(time.gmtime(0))
    print calendar.timegm(time.strptime('Jan 1, 2007 @ 00:00:00 UTC', '%b %d, %Y @ %H:%M:%S UTC'))
    print calendar.timegm(datetime.datetime.utcnow().utctimetuple())
    print time.ctime()
    print "Current date "  + time.strftime("%x")
    print datetime.date(2016,11,16)
    mytime = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    mytime = datetime.datetime(year=2016, month=11, day=16, hour=0, minute=0, second=0, microsecond=0)
    ts = int(time.mktime(mytime.utctimetuple()))
    print ts
    
    # Local time zone
    local = pytz.timezone("America/Denver")
    print "Local: ",local
    naive = datetime.datetime.strptime ("2016-9-22 22:30:00", "%Y-%m-%d %H:%M:%S")
    print "Naive: ",naive
    local_dt = local.localize(naive, is_dst=None)
    print "Local DT", local_dt
    utc_dt = local_dt.astimezone(pytz.utc)
    print "UTC DT", utc_dt
    print
    
    # Obtain the UTC Offset for the current system:
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    print "Offset is: ", UTC_OFFSET_TIMEDELTA
    local_datetime = datetime.datetime.strptime("2016-9-22 22:30:00", "%Y-%m-%d %H:%M:%S")
    result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
    print "Offset date: ", result_utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print
    
    mytime = datetime.datetime(year=2016, month=9, day=22, hour=22, minute=30, second=0, microsecond=0)
    ts = int(time.mktime(mytime.utctimetuple()))
    print "UTC:", ts
    datetuple = datetime.datetime.utcfromtimestamp(ts)
    datestr = datetuple.strftime('%Y-%m-%dT%H:%M:%SZ')
    print datestr
    print "Decagon:", 1474608600
    datetuple = datetime.datetime.utcfromtimestamp(1474608600)
    datestr = datetuple.strftime('%Y-%m-%dT%H:%M:%SZ')
    print datestr
    
    mystr =  unicode('W/m\u00b2','unicode-escape')
    print mystr
    """

#==========================================================================
# END
#==========================================================================
