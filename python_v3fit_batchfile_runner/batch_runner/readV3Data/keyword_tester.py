# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 12:46:39 2017

@author: Greg
"""


def keyword_tester(**kwargs):
    defined_keywords=['server','shotnum','tag','board_channel','channel']
    keywords_given=False
    
    # check that keywords are actually given
    if not len(kwargs):
        print("No keywords given in call")
        print(defined_keywords)
        return None

    # make sure all keywords are legal
    for key in kwargs:
        if key not in defined_keywords:
            print(key,"---Undefined Keyword in Call to get_data")
            print("Use: ",defined_keywords)
            return None
    
    # check that a shot number is given
    if 'shotnum' not in kwargs:
         print("no shot number given")
         return None
     
    # Check that either a tag, a board/channel pair, or a channel is given
    if 'tag' in kwargs:
        keywords_given=True
        print('tag given')
    elif 'board_channel' in kwargs:
        keywords_given=True
    elif 'channel' in kwargs:
        keywords_given=True
    else:
        print("get_data needs either a tag, a board/channel pair, ")
        print("or a single channel number")
        return 0
    
    return keywords_given
