# --------------------------------------
# ChannelInfo.py - Reads in the V3Data file
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
# Defines:  BoardNames 
#               links CTH board names with a number
#           Class ChannelInfo
#               Holds Channel boardnames, numbers and channel numbers
#           function channelToBoard
#               Converts channel number to ChannelInfo
#   
# 
#	
# Greg Hartwell
# 2017-11-27
#----------------------------------------------------------------------------

# Dictionary to link board numbers and names


class ChannelInfo(object):
    # Holds channel boardname,boardnumber and channelnumber
    
    BoardNames={0:"SCXI", \
            1:"Dtacq", \
            2:"Dtacq2", \
            3:"Dtacq3", \
            4:"Dtacq4", \
            5:"Dtacq5", \
            6:"Dtacq6", \
            7:"Dtacq7", \
            8:"Dtacq8"}
    
    def __init__(self,boardname,boardnumber,channelnumber):
        self.boardname=boardname
        self.boardnumber=boardnumber
        self.channelnumber=channelnumber
    # prints the information
    def printci(self):
        print("Channel Info: ",
              self.boardname, self.boardnumber,self.channelnumber)
    
    
def channelToBoard(channel):
    # Converts the channel to the board, channel pair
    if channel <= 24:
        board=0
    else:
        channel -= 24
        board = int((channel-1) / 96) +1
        channel = (channel-1) % 96 +1   
    return ChannelInfo(BoardNames[board],board,channel)

#Testing
#for i in range(1,300): ChannelInfo.channelToBoard(i).printci()





