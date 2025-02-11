#-----------------------------------------------------------------------------------------
# Following code is needed for print_line to work
#-----------------------------------------------------------------------------------------
from datetime import datetime
from datetime import timedelta, date

# The following needed "sudo pip install pytz tzlocal" to be run on the Linux box first
from pytz import timezone
import time

def time_now(in_tzStr):
  format = "%a %d%b%Y %H:%M:%S"
  now_utc = datetime.now(timezone('UTC'))
  now_asia = now_utc.astimezone(timezone(in_tzStr))
  return now_asia.strftime(format)
#-----------------------------------------------------------------------------------------
# End of time_now in 
#-----------------------------------------------------------------------------------------


def print_line(msg_parm):
    tz_str = 'Asia/Kolkata'
    pline = time_now(tz_str) + ': ' + msg_parm
    print(pline)
# end of print_line(msg_parm)
#-----------------------------------------------------------------------------------------
# End of print_line in 
#-----------------------------------------------------------------------------------------


