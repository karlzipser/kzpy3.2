from kzpy3.utils.common import *

second = 1.0
seconds = second
minute = 60*seconds
minutes = minute
hour = 60*minutes
hours = hour
day = 24*hours
days = day

"""

%a - abbreviated weekday name
%A - full weekday name
%b - abbreviated month name
%B - full month name
%c - preferred date and time representation
%C - century number (the year divided by 100, range 00 to 99)
%d - day of the month (01 to 31)
%D - same as %m/%d/%y
%e - day of the month (1 to 31)
%g - like %G, but without the century
%G - 4-digit year corresponding to the ISO week number (see %V).
%h - same as %b
%H - hour, using a 24-hour clock (00 to 23)
%I - hour, using a 12-hour clock (01 to 12)
%j - day of the year (001 to 366)
%m - month (01 to 12)
%M - minute
%n - newline character
%p - either am or pm according to the given time value
%r - time in a.m. and p.m. notation
%R - time in 24 hour notation
%S - second
%t - tab character
%T - current time, equal to %H:%M:%S
%u - weekday as a number (1 to 7), Monday=1. Warning: In Sun Solaris Sunday=1
%U - week number of the current year, starting with the first Sunday as the first day of the first week
%V - The ISO 8601 week number of the current year (01 to 53), where week 1 is the first week that has at least 4 days in the current year, and with Monday as the first day of the week
%W - week number of the current year, starting with the first Monday as the first day of the first week
%w - day of the week as a decimal, Sunday=0
%x - preferred date representation without the time
%X - preferred time representation without the date
%y - year without a century (range 00 to 99)
%Y - year including the century
%Z or %z - time zone or name or abbreviation
%% - a literal % character


"""

def time_str(mode='FileSafe'):
    now = datetime.datetime.now()
    if mode=='FileSafe':
       return now.strftime('%d%b%y_%Hh%Mm%Ss')
    if mode=='Pretty':
       return now.strftime('%A, %d %b %Y, %r')
    if mode=='TimeShort':
       return now.strftime('%H:%M')




class Timer:
    def __init__(self, time_s=0):
        self.time_s = time_s
        self.start_time = time.time()
        self.count = 0
    def check(self):
        #self.count += 1
        if time.time() - self.start_time > self.time_s:
            return True
        else:
            return False
    def c(self):
        #cr('*** warning, Timer.c() used ***',ra=1)
        return self.check()
    def time(self):
        return time.time() - self.start_time
    def reset(self):
        self.start_time = time.time()
        self.count = 0
    def trigger(self):
        self.start_time = 0
        #print("*** warning, trigger used ***")
        #raw_enter()
    def freq(self,name='',do_print=True):
        self.count += 1
        if self.check():
            value = self.count/self.time()
            if do_print:
                pd2s(name,'frequency =',dp(value,2),'Hz')
            self.reset()
            return value
        return False
    def message(self,message_str,color='grey',flush=False):
        if self.check():
            print(message_str+'\r'),
            #sys.stdout.flush()
            self.reset()
    def percent_message(self,i,i_max,flush=False):
        self.message(d2s(i,int(100*i/(1.0*i_max)),'%'),color='white')
    def wait(self):
        while not(self.check()):
            time.sleep(self.time_s/100.0)
        self.reset()   
Tr = Timer


exec(identify_file_str)

#EOF