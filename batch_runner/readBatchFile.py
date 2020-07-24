# --------------------------------------
# ReadBatchFile
# 
# BatchRunner Python project
# 
#
# Parameters:
#	 
# Returns:
#
# Example:
#
# Also defines:
#   BatchContents class
#   Shot_Times class
#
#   ParseLine
#
# To do:
#   gui file chooser?
#	
# Greg Hartwell
# 2017-11-21
#----------------------------------------------------------------------------

class BatchContents(object):
    
    # A structure to hold the information contained in the batch.cthsl file
    # defines typical get routines
    # defines a print routine
    # defines a count routine
    
    def __init__(self,filename):
        self.filename=filename
        
    def getFilename(self):
        return self.filename
    
    def getV3datafile(self):
        return self.v3dataFile
    
    def getV3configfile(self):
        return self.v3configFile
    
    def getShotTimeArray(self):
        return self.shot_time_array
    
    def print(self):
        print (self.filename)
        print (self.v3dataFile)
        print (self.v3configFile)
        for i in range(len(self.shot_time_array)):
            print (self.shot_time_array[i].shotnumber,\
                self.shot_time_array[i].time,\
                self.shot_time_array[i].dt)
    def count(self):
        return len(self.shot_time_array)
    
    def readBatchFile(self):
        
        shotTimeArray=[]
        with open(self.filename) as fp:
            for line in fp:
                if line:
                    chars=list(line)
                    if chars[0] != ';': # not a comment
                        # read in the files
                        if chars[0].isalpha():
                            if "v3Data" in line:
                                self.v3dataFile=line
                            else:
                                self.v3configFile=line
                        else:
                            #read in the shotnums,times and dts
                            if not line.isspace():
                                array=ParseLine(line)
                                if array[0] > 0:
                                    if len(array) == 3 :
                                        shotnum=array[0]
                                        ntimes=array[1]
                                        dt=array[2]
                                        shotTimeArray.append( \
                                            Shot_Times(shotnum,ntimes,dt))  
                                    else:
                                        #add time to last entry
                                        shotTimeArray[-1].addtime(array[0]) 
        self.shot_time_array=shotTimeArray                             
#------------------------------------------------------------------

class Shot_Times(object):
    # this holds the shot number, reconstruction time and averaging time
    def __init__(self,shotnumber,time,dt):
        self.shotnumber=shotnumber
        self.time=[]
        self.dt=dt
    def printst(self):
        print(self.shotnumber,self.time,self.dt)
    def addtime(self,time):
        self.time.append(time)
#--------------------------------------------------------------------
        
def ParseLine(line):
    # takes a line of integers and float and returns
    # and list of the values
    values=[]
    line=line.strip(' \r\n')
    chars=line.split(" ")
    for c in chars:
        c=c.strip()
        if c.isdigit():
            num=int(c)
            values.append(num)
        else:
            if c:
                num=float(c)
                values.append(num)       
    return values
#----------------------------------------------------------------------

#------------------------------------------------------------------------                 

