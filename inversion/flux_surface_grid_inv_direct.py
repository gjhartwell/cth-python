# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:36:06 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from vmec import wout_file, get_fluxsurface_RZ_stheta, plot_array_on_flux_surfaces
from scipy.interpolate import griddata
from pathlength import Pathlength2D
from shapely.geometry import Polygon, LineString

def array_to_tuple(point):
    # point in array to point in tuple
    new_point = (point[0], point[1])
    return new_point


def find_closest_index(array, value):
    new_array = abs(array - value)
    try:
        index = new_array.argmin()
    except:
        print('Invalid Array')
        index = 0
    return int(index)

        
class FluxSurfaceGrid:
    
    def __init__(self, wout_filepath,
                 n_theta=100,
                 phi=252,
                 size=301):
        self.wout = wout_file(wout_filepath)
        self.n_theta = n_theta
        self.phi = phi
        self.size = size
        #self.make_grid()
        
        
    def make_grid(self):
        R, Z, s_grid, theta_grid = get_fluxsurface_RZ_stheta(self.wout.ns,
                                                             self.wout.rmnc, 
                                                             self.wout.zmns,
                                                             self.wout.xm, 
                                                             self.wout.xn, 
                                                             self.n_theta,
                                                             self.phi)
        
        self.theta = np.linspace(0, 2*np.pi, self.n_theta)
        self.s = self.wout.s
        self.vmec_R, self.vmec_Z = R, Z
        
        self.pathlength2d = Pathlength2D(R, Z)
        
        self.s_grid, self.theta_grid = s_grid[0:], theta_grid
        

        f = np.zeros([len(self.vmec_R), len(self.vmec_R[0])])


        del_R = (R[-1] - R[-2])*.1 + R[-1]
        del_Z = (Z[-1] - Z[-2])*.1 + Z[-1] 

        R = np.concatenate([R,[del_R]])
        Z = np.concatenate([Z,[del_Z]])

        zeros = np.zeros(len(f[-1]))
        f = np.concatenate([f,[zeros]])
        ff = np.ndarray.flatten(f)

        self.Rf = np.ndarray.flatten(R).tolist()
        self.Zf = np.ndarray.flatten(Z).tolist()
        
        
        c = [[i,j] for i,j in zip (self.Rf, self.Zf)]
        self.c = c   
        grid = {}

        R_max, R_min = round(max(R[-1])+.05,1),round(min(R[-1])-.05,1)
        Z_max, Z_min = round(max(Z[-1])+.05,1),round(min(Z[-1])-.05,1)
    

        R_half = round(R_max-R_min,2)/2

        if Z_max>R_half or Z_min<-1*R_half:
            print('Grid not squared properly')
            raise
            

        grid['x_min']= R_min
        grid['x_max']= R_max
        grid['x_size']=complex(self.size)
        
        
        grid['y_min']=-1*R_half 
        grid['y_max']=R_half
        grid['y_size']=complex(self.size)


        grid['x'],grid['y']=np.mgrid[grid['x_min']:grid['x_max']:grid['x_size'],grid['y_min']:grid['y_max']:grid['y_size']]

        grid['x_step']=grid['x'][1][0]-grid['x'][0][0]
        grid['y_step']=grid['y'][0][1]-grid['y'][0][0]

        grid['grid_data']=griddata(c,ff,(grid['x'],grid['y']),method='nearest')     
        #grid['grid_data']=griddata(c,ff,(grid['x'],grid['y']),method='cubic')     
    
        self.grid = grid

        return

    def refine_grid(self, grid_data, grid_x, grid_y):
        c = [[i,j] for i,j in zip(np.ndarray.flatten(grid_x), np.ndarray.flatten(grid_y))]
        ff = np.ndarray.flatten(grid_data)
        
        f_zero = np.ones(self.s_grid.shape)
        self.update_grid_from_array(f_zero)
        self.zero_grid = self.grid['grid_data']
        
        
        
        #self.grid['grid_data']=griddata(c,ff,(self.grid['x'],self.grid['y']),method='nearest')#*self.zero_grid
        self.grid['grid_data']=griddata(c,ff,(self.grid['x'],self.grid['y']),method='linear')#*self.zero_grid
        
        
        
        return
        

    def update_grid_from_array(self,f):
        # f is the function evaluated on the grid
        # f is a function of theta and s
        zeros = np.zeros(len(f[-1]))
        f = np.concatenate([f,[zeros]])            
        ff = np.ndarray.flatten(f)

        self.grid['grid_data'] = griddata(self.c,ff,(self.grid['x'],self.grid['y']),method='nearest')  
        #self.grid['grid_data'] = griddata(self.c,ff,(self.grid['x'],self.grid['y']),method='cubic')  
        
        return


    def update_grid_from_flux_array(self,f,s):
        # f is the function evaluated on the grid
        # f is a function of theta and s
        
        
        values = np.interp(self.s, s, f)
        
        f = values[:,np.newaxis]*np.ones(self.n_theta)
        
        zeros = np.zeros(len(f[-1]))
        f = np.concatenate([f,[zeros]])            
        ff = np.ndarray.flatten(f)

        self.grid['grid_data'] = griddata(self.c,ff,(self.grid['x'],self.grid['y']),method='nearest')  
        #self.grid['grid_data'] = griddata(self.c,ff,(self.grid['x'],self.grid['y']),method='cubic')  
        
        return    


    def update_grid_from_s_theta_array(self, s_theta_array):
        zeros = np.zeros(len(s_theta_array[0]))
        f = np.concatenate([s_theta_array, [zeros]])
        ff = np.ndarray.flatten(f)
        self.grid['grid_data'] = griddata(self.c,ff,(self.grid['x'],self.grid['y']),method='nearest')  
        return
        
    
    def get_s_theta_points(self):
        c2 = [[i,j] for i,j in zip (np.ndarray.flatten(self.grid['x']), np.ndarray.flatten(self.grid['y']))]
        self.c2 = c2 
        
        ff = np.ndarray.flatten(self.grid['grid_data'])
        #print(len(c2), len(ff))
        
        s_theta_array = griddata(self.c2, ff,(self.vmec_R, self.vmec_Z), method='nearest')
        self.s_theta_array = s_theta_array
        return 
        
    



    def get_mulitple_chord_pathlengths_points(self, points):
        O, D = [], []
        
        for kk in range(len(points)):
            p1 = points[kk][0]
            p2 = points[kk][1]
            
            O.append(p1)
            d = np.array(p2) - np.array(p1)
            d = d/np.linalg.norm(d)
            D.append(d.tolist())
            
        master = self.get_multiple_chord_pathlengths(O, D)
        return master
    

    def get_multiple_chord_pathlengths(self, O_array, D_array):
        master = []
        for O, D in zip(O_array, D_array):
            master.append(self.get_chord_pathlengths(O, D)['matrix'])

        return np.array(master)
    

    def get_chord_pathlengths(self,O,D):
        chord = {}        
        #print(O, D)

        int_points =self.pathlength2d.outersect(O, O+D)
        
        
        if int_points==None:
            #print('Outersect Failed',O,D)
            chord['matrix'] = np.zeros((self.size, self.size))
            chord['O'] = O
            chord['D'] = D

            return chord
        

        xn_ind1 = find_closest_index(self.grid['x'][:,0],int_points[0][0])
        xn_ind2 = find_closest_index(self.grid['x'][:,0],int_points[1][0])
        
        yn_ind1 = find_closest_index(self.grid['y'][0],int_points[0][1])
        yn_ind2 = find_closest_index(self.grid['y'][0],int_points[1][1])
          

        xn_max_lcf, xn_min_lcf = max(xn_ind1, xn_ind2), min(xn_ind1, xn_ind2)
        yn_max_lcf, yn_min_lcf = max(yn_ind1, yn_ind2), min(yn_ind1, yn_ind2)
        
        
        grid = self.grid
        D = D/np.linalg.norm(D)
        
        grid_corners = np.array([array_to_tuple([grid['x_min'],grid['y_min']]),
                                 array_to_tuple([grid['x_min'],grid['y_max']]),
                                 array_to_tuple([grid['x_max'],grid['y_max']]),
                                 array_to_tuple([grid['x_max'],grid['y_min']])])
        
    
    
        
        grid_outer = Polygon(grid_corners)
        
        line = LineString([O, O+D])
        
        
        inter_points = list(grid_outer.intersection(line).coords)
        
        
        int0 = O - inter_points[0]
        int1 = O - inter_points[1]
        
        d0 = np.dot(int0, int0)
        d1 = np.dot(int1, int1)


        if d0 < d1:
            O = np.array(inter_points[0])   
        else:
            O = np.array(inter_points[1])             

        
        P = O - np.array([grid['x_min'],grid['y_min']])
        

        cell_n = [(P[0]/grid['x_step'])//1,(P[1]/grid['y_step'])//1]
        
        deltx = grid['x_step']/D[0]
        delty = grid['y_step']/D[1]


        if D[0] >= 0:     
            tx0 = ((cell_n[0]+1)*grid['x_step']-P[0])/D[0]   
            xn_sign = 1
        else:
            tx0 = ((cell_n[0])*grid['x_step']-P[0])/D[0]
            xn_sign = -1
   
        if D[1] >= 0:
            ty0 = ((cell_n[1]+1)*grid['y_step']-P[1])/D[1]
            yn_sign = 1
        else:
            ty0 = ((cell_n[1])*grid['y_step']-P[1])/D[1]
            yn_sign = -1
        
        
        t = []
        xn = [0]
        yn = [0]
        ii = 0
        
        max_xn = (len(grid['x'])-cell_n[0]) #-1
        max_yn = (len(grid['y'])-cell_n[1]) #-1
        
        min_xn = -1*cell_n[0]
        min_yn = -1*cell_n[1]
        
        while (min_xn <= xn[-1] <= max_xn) and (min_yn <= yn[-1] <= max_yn):
            tx = tx0 + deltx*xn[ii]
            ty = ty0 + delty*yn[ii]
            #print(tx, ty)
            
            if tx < ty:
                xn.append(xn[ii]+1*xn_sign)
                yn.append(yn[ii])
                t.append(tx)
            else:
                xn.append(xn[ii])
                yn.append(yn[ii]+1*yn_sign)
                t.append(ty)
        
            ii+=1

        del_t = []

            
        xn = xn + cell_n[0]
        yn = yn + cell_n[1]
    
        for jj in range(0, len(t)-1):
            value = t[jj+1] - t[jj]
            del_t.append(value)
    
        chord['O'] = O
        chord['D'] = D
        chord['t'] = t
        chord['del_t'] = del_t
        chord['xn'] = xn
        chord['yn'] = yn

        matrix = np.zeros((self.size, self.size))

        for i, value in enumerate(del_t):
            if (xn_min_lcf-1 <= xn[i]-1 <= xn_max_lcf+1) and (yn_min_lcf-1 <= yn[i]-1 <= yn_max_lcf+1):
                matrix[int(xn[i]-1),int(yn[i]-1)] = value
            else:
                matrix[int(xn[i]-1),int(yn[i]-1)] = 0
                
        chord['matrix'] = matrix

        #self.plot_cell(chord)
        #self.plot_vector(chord)

        return chord

    
    def evaluate_single_signal(self, chord_matrix):
        #value = sum(sum(chord_matrix*self.grid['grid_data']))
        value = np.einsum('ij,ij->',chord_matrix,self.grid['grid_data'])

        return value


    def evaluate_signals(self, chord_matrix_list):
         values = np.einsum('aij,ij->a',chord_matrix_list,self.grid['grid_data'])
         return values

    
    def plot_grid(self,title=None,surfaces=False,cbar_label=None, contours=None):
        grid = self.grid
        #plt.figure()
        plt.pcolormesh(grid['x'],grid['y'],grid['grid_data'],cmap='gnuplot2')
        cbar = plt.colorbar()
        labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
        cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')
        plt.xlim([.55, 1.05])
        plt.ylim([-.25, .25])
        
        #plt.xlim([grid['x_min'], grid['x_max']])
        #plt.ylim([grid['y_min'], grid['y_max']])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlabel('R (m)',fontsize = 15, weight ='bold')
        plt.ylabel('Z (m)',fontsize = 15, weight ='bold')
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')
        
        if contours:
            plt.contour(grid['x'], grid['y'], grid['grid_data'])
        
        if title:
            plt.title(title,fontsize=13,weight='bold')
        if surfaces:
            for ii in range(len(self.vmec_R)):
                plt.plot(self.vmec_R[ii], self.vmec_Z[ii], 'r', linestyle='--')
            plt.plot(self.vmec_R[-2], self.vmec_Z[-2], 'k', linestyle='--')
        if cbar_label:            
            cbar.set_label(cbar_label, rotation=270,fontsize=13, weight='bold', labelpad=15)
        else:
            cbar.set_label('Relative Intensity', rotation=270,fontsize=13, weight='bold',labelpad=15)
            
            
            
    def plot_vector(self,chord):
        O = chord['O']
        D = chord['D']  
        p1 = O
        p2 = O+D
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]], 'r')

        

    def plot_vector_points(self, chord):
        O = chord['O']
        D = chord['D']
        tt= chord['t']
        for t in tt:
            points = O+D*t
            plt.scatter(points[0],points[1],c='w',s=10)


    def plot_rect(self, x, y, x_size,y_size):
        xpoints = [x, x, x+x_size, x+x_size, x]
        ypoints = [y, y+y_size, y+y_size, y, y]
        #print(x, y)
        plt.plot(xpoints,ypoints, 'r', linewidth=1)


    def plot_cell(self, chord):   
        xn = chord['xn']
        yn = chord['yn']
        grid = self.grid
        for ii in range(len(xn)):
            
            self.plot_rect((xn[ii])*grid['x_step']+grid['x_min'],
                     (yn[ii])*grid['y_step']+grid['y_min'],
                     grid['x_step'], 
                     grid['y_step'])
    

    def local_gaussian_polar2(self, A,  mu, sigma, theta_mu, s, theta):
        #A = 2.3548*sigma*10
        #A = 1 / np.sqrt(2*np.pi*sigma**2)
        
        B = -1*(s-mu)**2/(2*(sigma**2)) 
        B = np.exp(B)[:,np.newaxis] * np.ones(len(theta))
        
        theta_1 = np.sin(.5*(theta-theta_mu))
        
        #C = ((s[:,np.newaxis]**2)*((theta_1**2)/(2*sigma**2)))
        C = (np.ones(len(s))[:,np.newaxis]*((theta_1**2)/(2*sigma**2)))
        C = np.exp(-1*C)
        
        value = A*B*C
        return value
