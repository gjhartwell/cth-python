# -----------------------------------------------------------------
#
# PreprocessV3DataFile
# 
# preprocesses the x.v3Data file to make it easier to interpret
# removes blank space
# removes comments
# removes ',' (commas)
# combines multi-line entries into single-line entries
#
#
# Greg Hartwell
#
# 2017-11-27
# 2020-07-28 added debug flag to print diagnostic information
#------------------------------------------------------------------

def PreprocessV3DataFile(filein,debug):
    # first pass
    # remove '#' comments
    filein=filein.strip('\n')
    fileout1=filein+"temp"
    fout1=open(fileout1,'w')
    fin=open(filein,'r')
    for line in fin:
        chars=list(line)
        if chars[0]  != '#': # not a comment
            if not line.isspace():
                if not "#" in line:
                    fout1.write(line)
                else:
                    parts=line.split('#')
                    fout1.write(parts[0])
                    fout1.write('\r')
    fin.close()
    fout1.close()
    
    # second pass 
    # modify to create single lines of code
    #     from those ending in paretheses

    # need to read all the lines so they can be concatenated later
    
    fin=open(fileout1,'r')
    lines=[]
    for line in fin:
        lines=lines+[line]
    fin.close()
   
    stack=[]
    numParenthesis=0
    numBrackets=0
    newlines=[]
    inPStack=False
    inBStack=False
    for line in lines:
        if debug: print(line)
        line=line.replace('LOAD_CHANNEL_NUMBER','LOAD_CHANNEL_NUMBER ')
        line=line.replace('LOAD_CHANNEL(','LOAD_CHANNEL (')
        line=line.replace('MULTIPLY','MULTIPLY ')
        line=line.replace('NUMBER','NUMBER ')
        if lastPrintableChar(line) == "(":
            numParenthesis+=1
            inPStack=True
            stack.insert(0,line)
        elif inPStack:   
            stack.insert(0,line)
            numParenthesis+=countParenthsis(line)
            if inPStack and numParenthesis==0:
                inPStack=False
                stack.reverse()
                if debug: print("stack is ",stack)
                newline=[]
                for line in stack:
                    chars=list(line)
                    line=''.join(chars[:-1])
                    newline+=line
                
                stack=[]
                newline=''.join(newline)
                #remove extra white space
                newline=' '.join(newline.split())
                newline=newline+'\n'
                if debug: print('newline is ',newline)
                newlines+=[newline]
        
        elif lastPrintableChar(line) == "{":
            numBrackets+=1
            if debug: print("Brackets ",numBrackets)
            inBStack=True
            stack.insert(0,line)
        elif inBStack:   
            stack.insert(0,line)
            numBrackets+=countBrackets(line)
            if inBStack and numBrackets==0:
                inBStack=False
                stack.reverse()
                if debug: print("stack is ",stack)
                newline=[]
                for line in stack:
                    chars=list(line)
                    line=''.join(chars[:-1])
                    newline+=line
                
                stack=[]
                newline=''.join(newline)
                #remove extra white space
                newline=' '.join(newline.split())
                newline=newline+'\n'
                if debug: print('newline is ',newline)
                newlines+=[newline]
        else:        
            newlines+=[line]
    
    #output the new lines
    fileout2=fileout1+"2"
    fout2=open(fileout2,'w')
    for line in newlines:
        fout2.write(line)    
    fout2.close()
    if debug: 
        print("==============================================================")
        print("FINISHED PREPROCESSING")
        print("==============================================================")
        print("")
    
    return fileout2

import string
def lastPrintableChar(line):
    # finds the last printable, non-whitespace character in a line
    
    chars=list(line)
    # get printable charcters that are not whitespace
    printableChars=[]
    for c in chars:
        if c in string.printable:
            if c not in string.whitespace:
                printableChars+=[c]
    return printableChars[-1]

def countParenthsis(line):
    count=line.count('(')-line.count(')')
    return count

def countBrackets(line):
    count=line.count('{')-line.count('}')
    return count   
    
                
    

# Testing
#filein="C:/Users/Greg/Documents/Reconstructions/Ennis_180122/phiedge_only.v3data"
#   
#fileout=PreprocessV3DataFile(filein)
#print(fileout)