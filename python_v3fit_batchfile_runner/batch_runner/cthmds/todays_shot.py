# -*- coding: utf-8 -*-
# --------------------------------------
# todays_shot.py
# 
# MDSplus Python project
# for CTH data access
#
# 	todays_shot --- returns true if a shotnumber is from the current date  
#
# Parameters:
#	shotnum - integer - the shotnumber to open
# Returns:
#	boolean - true if shotnumber is from the current date
#
# Example:
#       boolean_return=todays_shot(shotnum)
#
# Also defines:
#	
# Greg Hartwell
# 2016-12-16
#----------------------------------------------------------------------------
import time
	
def todays_shot(shotnum):
    shotString=str(shotnum)
    shotDate=shotString[0:6]

	# get the date in the format YYMMDD
    todayYear=time.strftime("%Y")
    todayYear=todayYear[2:4]
    todayMonth=time.strftime("%m")
	# need to check if date is 04 or 4
    todayDay=time.strftime("%d")
    today=todayYear+todayMonth+todayDay

    if today == shotDate:
        from_today = True
    else:
        from_today = False

    return from_today
# ---------------------------------------------------------------------------
