# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:43:39 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import sqlite3
from sqlite3 import Error
import numpy as np
import json

v3fit_recon_location = "/home/cth/cthgroup/Python/recon/database/v3fit_reconstruction.db"
v3fit_results_location = "/home/cth/cthgroup/Python/recon/database/v3fit_results.db"
v3fit_db_location_win = "Z:/Python/recon/database/v3fit_results.db"

#v3fit_db_location_win = "\database\v3fit_res.db"



class ReconResults:
     
    def __init__(self, query, input1):
        
        self.query = query
        self.input = input1
        
        
        #rows = generic_query_results(query, input1)

    def select_results(self, query, input1):
        rows = generic_query_results(query, input1)
        row = rows[0]

        
        self.shot = row[1]
        self.pcurr_type = row[2]
        self.pmass_type = row[3]

        self.times = json.loads(row[4])
        self.AC = json.loads(row[5])
        self.AM = json.loads(row[6])
        self.iota_vac = json.loads(row[7])
        self.iota = json.loads(row[8])
        self.raw_density = json.loads(row[9])
        self.raw_plasma_current = json.loads(row[10])
        self.curtor = json.loads(row[11])
        self.pp_ne_as = json.loads(row[12])
        self.pp_ne_af = json.loads(row[13])
        self.pp_sxrem_as = json.loads(row[14])
        self.pp_sxrem_af1= json.loads(row[15])
        self.pp_sxrem_af2= json.loads(row[16])
        self.pres_scale = json.loads(row[17])
        self.z_offset = json.loads(row[18])
        self.phiedge = json.loads(row[19])
        self.rmnc = json.loads(row[20])
        self.zmns = json.loads(row[21])
        self.xm = json.loads(row[22])
        self.xn = json.loads(row[23])
        self.chi_squared = json.loads(row[24])
        self.s = json.loads(row[25])
        self.Rmajor = json.loads(row[26])
        self.Aminor = json.loads(row[27])
        self.sxr = json.loads(row[28])
        self.bolo = json.loads(row[29])
        self.wout_location = json.loads(row[30])
        self.volume_p = json.loads(row[31])
        
        
        
"""      
        

def grab_recon_results(query, input1):
    rows = generic_query_results(query, input1)
    
    row = rows[0]

tp_times = json.loads(tp[1])
tp_AC = json.loads(tp[2])
tp_iota_vac = json.loads(tp[3])
tp_chi = json.loads(tp[4])
tp_rmnc = json.loads(tp[5])
tp_zmns = json.loads(tp[6])
tp_xm= json.loads(tp[7])
tp_xn = json.loads(tp[8])
tp_iota = json.loads(tp[9])

"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        #print('Here')
        return conn
    except Error as e:
        print(e)
 
    return 


def update_recon_database(recon_names, shot, times, window, full_shot, locations, recon_user):
    database = v3fit_recon_location
    
    conn = create_connection(database)
    
    sql_insert = """ INSERT INTO reconstructions(name,shot,time,window,full_shot,fs_id,location,recon_runner)
                     VALUES(?,?,?,?,?,?,?,?)"""
    
    if full_shot:
        last_fs_id_query = "SELECT fs_id FROM reconstructions ORDER BY id DESC LIMIT 10"
        last_fs_id_query = "SELECT fs_id FROM reconstructions WHERE fs_id IS NOT NULL ORDER BY id DESC LIMIT 1"
        #last_fs_id_query = "SELECT name (SELECT fs_id FROM reconstructions WHERE name=pc.name AND fs_id IS NOT NULL ORDER BY id DESC LIMIT 1) as fs_id"
        with conn:
            c = conn.cursor()
            c.execute(last_fs_id_query)
            last_fs_id = c.fetchone()[0]
            
            for i in range(len(recon_names)):
                new_recon_input = (recon_names[i], shot, times[i], window, 1, int(last_fs_id)+1, locations[i], recon_user)
    
                c.execute(sql_insert, new_recon_input)
                
            
            
    else:
        with conn:
            c = conn.cursor()
            for i in range(len(recon_names)):
                new_recon_input = (recon_names[i], shot, times[i], window, 0, None, locations[i], recon_user)
    
                c.execute(sql_insert, new_recon_input)
            
          

    return  








def generic_query_results(query, inputs, windows=False):
    
    if windows:
       conn = create_connection(v3fit_db_location_win)
   
    else:
       conn = create_connection(v3fit_results_location)
        
    with conn:
        cur = conn.cursor()
        cur.execute(query,inputs)
        
        rows = cur.fetchall()
        
        
    return rows






def select_recon_by_shotnumber(shotnumber):
    conn = create_connection(v3fit_recon_location)
    
    with conn:
        cur = conn.cursor()
        query = "SELECT * FROM reconstructions WHERE shot=?"
        cur.execute(query,(shotnumber,))
        
        rows = cur.fetchall()
        

    return rows

    

def select_recon_by_shotnumber_and_fs_id(shotnumber,fs_id=None):
    conn = create_connection(v3fit_recon_location)
    
    with conn:
        cur = conn.cursor()
        query = "SELECT MAX(fs_id) FROM reconstructions WHERE shot=?"
        cur.execute(query,(shotnumber,))
        
        max_fs_id = cur.fetchall()[0][0]
        
        
        query = "SELECT shot,time,window,full_shot,location FROM reconstructions WHERE fs_id=?"
        
        if fs_id==None:
            cur.execute(query,(max_fs_id,))
        else:
            cur.execute(query,(fs_id,))
        
        rows = cur.fetchall()
          
    return rows


def get_recon_shotnumbers():
    conn = create_connection(v3fit_recon_location)
    
    with conn:
        cur = conn.cursor()
        query = "SELECT DISTINCT shot FROM reconstructions"
        cur.execute(query)
        
        rows = cur.fetchall()    
    
    
    
    return rows



def insert_results(conn, results):
    sql = """INSERT INTO results(shot,pcurr_type,pmass_type,times,AC,AM,iota_vac,
                                 iota,raw_density,raw_plasma_current,curtor,
                                 pp_ne_as,pp_ne_af,
                                 pp_sxrem_as,pp_sxrem_af1,pp_sxrem_af2,
                                 pres_scale,z_offset,phiedge,rmnc,zmns,xm,xn,chi_squared,s,
                                 Rmajor, Aminor, sxr, bolo, wout_location, volume_p)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            

    cur = conn.cursor()
    cur.execute(sql, results)
    print(cur.lastrowid)
    return



def results_to_database(shot, pcurr_type, pmass_type, times, AC, AM, iota_vac, iota,
                        raw_density, raw_plasma_current, curtor, pp_ne_as, pp_ne_af,
                        pp_sxrem_as, pp_sxrem_af1, pp_sxrem_af2,
                        pres_scale, z_offset, phiedge, rmnc, zmns, xm, xn,
                        chi_squared,s,Rmajor, Aminor, sxr, bolo, wout_location,
                        volume_p):
    
    database = v3fit_results_location
    conn = create_connection(database)
    
    times = json.dumps(times)
    AC = json.dumps(AC)
    AM = json.dumps(AM)
    iota_vac = json.dumps(iota_vac)
    iota = json.dumps(iota)
    raw_density = json.dumps(raw_density)
    raw_plasma_current = json.dumps(raw_plasma_current)
    curtor = json.dumps(curtor)
    pp_ne_as = json.dumps(pp_ne_as)
    pp_ne_af = json.dumps(pp_ne_af)
    pp_sxrem_as = json.dumps(pp_sxrem_as)
    pp_sxrem_af1 = json.dumps(pp_sxrem_af1)
    pp_sxrem_af2 = json.dumps(pp_sxrem_af2)
    pres_scale = json.dumps(pres_scale)
    z_offset = json.dumps(z_offset)
    phiedge = json.dumps(phiedge)
    rmnc = json.dumps(rmnc)
    zmns = json.dumps(zmns)
    xm = json.dumps(xm)
    xn = json.dumps(xn)
    chi_squared = json.dumps(chi_squared)
    s = json.dumps(s)
    Rmajor = json.dumps(Rmajor)
    Aminor = json.dumps(Aminor)
    sxr = json.dumps(sxr)
    bolo = json.dumps(bolo)
    wout_location = json.dumps(wout_location)
    volume_p = json.dumps(volume_p)
    
    result = (shot, pcurr_type, pmass_type, times, AC, AM, iota_vac, iota,
              raw_density, raw_plasma_current, curtor, pp_ne_as, pp_ne_af,
              pp_sxrem_as, pp_sxrem_af1, pp_sxrem_af2,
              pres_scale, z_offset, phiedge, rmnc, zmns, xm, xn,
              chi_squared,s, Rmajor, Aminor, sxr, bolo, wout_location,
              volume_p)
    
    with conn:
        insert_results(conn, result)
        
    print('Done')
    
    return
#select_recon_by_shotnumber_and_fs_id(14092626) 
    
    
 
    





def select_time_ac_iotavac(windows=True):
   query = "SELECT shot, times, AC, iota_vac FROM results"
   
   if windows:
       database = v3fit_db_location_win
   else:
       database = v3fit_results_location

   conn = create_connection(database)
   with conn:
       c = conn.cursor()
       c.execute(query)
       
       rows = c.fetchall()
       
       
   return rows



#print('Here')
#print(select_time_and_ac(v3fit_db_location_win))


    
    
    
    