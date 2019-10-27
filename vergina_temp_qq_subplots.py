#!/usr/bin/python3

""" This program plots the temperature (mean, max, min) quantiles per 5% (Q-Q plots) for each subregion and simulation. """


# round to the nearest multiple of 5
def myround(x, base=5):
    return base * round(x/base)


import numpy as np
from netCDF4 import Dataset
from netCDF4 import num2date
import matplotlib.pyplot as plt
from math import modf
import matplotlib.ticker as plticker


path1 = '/mnt/meteo/groups/postproc/hindcast_WRF381c_VERGINA/from_wrfxtrm_d02_TEMP/wrf0.11_to_wrf0.44/regions/'     # WRF 0.11 remmapped to 0.44
path2 = '/mnt/meteo/groups/postproc/hindcast_WRF381c_VERGINA/from_wrfxtrm_d01_TEMP/eobs0.1_to_wrf0.44/regions/eobs/'# Eobs 0.11 remapped to 0.44
path3 = '/mnt/meteo/groups/postproc/hindcast_WRF381c_VERGINA/from_wrfxtrm_d01_TEMP/eobs0.1_to_wrf0.44/regions/wrf/' # WRF 0.44
path4 = '/mnt/meteo/groups/meteo_student/lucas/lucas_0.44_cdo/regions/'                                             # Lucas 0.44 remapped to 0.44 

names = ['AL', 'BI', 'EA', 'FR', 'IP', 'MD', 'ME', 'SC']
temp = ['tg', 'tx', 'tn']
temperatures = ['Tmean', 'Tmax', 'Tmin']
seasons = ['DJF', 'MAM', 'JJA', 'SON']

seas_daytemp_eobs = np.nan*np.zeros((3,8,4,1748))
seas_daytemp_wrf11 = np.nan*np.zeros((3,8,4,1748))
seas_daytemp_wrf44 = np.nan*np.zeros((3,8,4,1748))
seas_daytemp_lucas = np.nan*np.zeros((3,8,4,1748))
        

#  tmean, tmax, tmin
for t in range(3):
    # regions
    for reg in range(8):

        fullpath1 = path1 + names[reg] + '_' + temp[t] + '_wrf.nc'                        # WRF 0.11
        fullpath2 = path2 + names[reg] + '_' + temp[t] + '_eobs.nc'                       # EOBS 
        fullpath3 = path3 + names[reg] + '_' + temp[t] + '_wrf.nc'                        # WRF 0.44
        fullpath4 = path4 + names[reg] + '_' + temp[t] + '_LUCAS_daymean_1990-2008.nc'   # LUCAS 0.44
        
        # read data
        data1 = Dataset(fullpath1, 'r')
        data2 = Dataset(fullpath2, 'r')
        data3 = Dataset(fullpath3, 'r')
        data4 = Dataset(fullpath4, 'r')
        
        daytemp_wrf11 = np.array(data1.variables[temp[t]])
        daytemp_eobs = np.array(data2.variables[temp[t]])
        daytemp_wrf44 = np.array(data3.variables[temp[t]])
        daytemp_lucas = np.array(data4.variables[temp[t]])
        
        # nan values
        daytemp_eobs[daytemp_eobs<=-9999] = np.nan
        daytemp_wrf11[daytemp_wrf11<=-9999] = np.nan
        daytemp_wrf44[daytemp_wrf44<=-9999] = np.nan
        daytemp_lucas[daytemp_lucas<=-9999] = np.nan

        daytemp_wrf11 = daytemp_wrf11-273.15

        x = data3.variables['XLONG'][:,:] # 2D: y,x
        y = data3.variables['XLAT'][:,:]

        time2 = data2.variables['time']
        #convert time(s) to date andtime
        datetime=num2date(time2[:], time2.units)  
        np.array(datetime)
       

        time_lucas = data4.variables['time']
        #convert time(s) to date andtime                                                                                                    
        datetime_lucas=num2date(time_lucas[:], time_lucas.units)
        np.array(datetime_lucas)
        
       # turn many x,y points into a single one for each region
        reg_temp_wrf11 = np.nanmean(daytemp_wrf11, axis=(1,2))
        reg_temp_eobs = np.nanmean(daytemp_eobs, axis=(1,2))
        reg_temp_wrf44 = np.nanmean(daytemp_wrf44, axis=(1,2))
        reg_temp_lucas = np.nanmean(daytemp_lucas, axis=(1,2))

        # seperate seasonal daily values
        count1=count2=count3=count4=0
        i1=i2=i3=i4=0

        for j in range(len(datetime)-31): # exclude December 2008
            
            if datetime[j].month==1 or datetime[j].month==2 or datetime[j].month==12:
                seas_daytemp_wrf11[t,reg,0,i1] = reg_temp_wrf11[j]
                seas_daytemp_eobs[t,reg,0,i1] = reg_temp_eobs[j]
                seas_daytemp_wrf44[t,reg,0,i1] = reg_temp_wrf44[j]  # djf
                seas_daytemp_lucas[t,reg,0,i1] = reg_temp_lucas[j]
                count1+=1
                i1+=1

            elif datetime[j].month==3 or datetime[j].month==4 or datetime[j].month==5:
                seas_daytemp_wrf11[t,reg,1,i2] = reg_temp_wrf11[j]
                seas_daytemp_eobs[t,reg,1,i2] = reg_temp_eobs[j]
                seas_daytemp_wrf44[t,reg,1,i2] = reg_temp_wrf44[j]
                seas_daytemp_lucas[t,reg,1,i2] = reg_temp_lucas[j] # mam
                count2+=1
                i2+=1

            elif datetime[j].month==6 or datetime[j].month==7 or datetime[j].month==8:
                seas_daytemp_wrf11[t,reg,2,i3] = reg_temp_wrf11[j]
                seas_daytemp_eobs[t,reg,2,i3] = reg_temp_eobs[j]
                seas_daytemp_wrf44[t,reg,2,i3] = reg_temp_wrf44[j] 
                seas_daytemp_lucas[t,reg,2,i3] = reg_temp_lucas[j] # jja
                count3+=1
                i3+=1

            elif datetime[j].month==9 or datetime[j].month==10 or datetime[j].month==11:
                seas_daytemp_wrf11[t,reg,3,i4] = reg_temp_wrf11[j]
                seas_daytemp_eobs[t,reg,3,i4] = reg_temp_eobs[j]
                seas_daytemp_wrf44[t,reg,3,i4] = reg_temp_wrf44[j] # son
                seas_daytemp_lucas[t,reg,3,i4] = reg_temp_lucas[j]
                count4+=1
                i4+=1

           
        count=[count1,count2,count3,count4] # count for all wrf, eobs and lucas tas

#################################################################################

for t in range(3):
    quant = np.nan*np.zeros((19))
    a = np.nan*np.zeros((19))
    b = np.nan*np.zeros((19))
    q_eobs = np.nan*np.zeros((19))
    q_wrf11 = np.nan*np.zeros((19))
    q_lucas = np.nan*np.zeros((19))
    q_wrf44 = np.nan*np.zeros((19))
    
    for seas in range(4):
        
        fig,ax = plt.subplots(3,3, figsize=(20,18))
        ax[-1,-1].axis('off')

        for reg in range(8):
                     
            if reg<=2:
                row=0
            elif reg<=5: 
                row=1
            elif reg<=7:
                row=2
                
            if reg==0 or reg==3 or reg==6:
                col=0
            elif reg==1 or reg==4 or reg==7:
                col=1
            elif reg==2 or reg==5:
                col=2

            print(row,col)    

            # sorting
            seas_daytemp_eobs_sort = np.sort(seas_daytemp_eobs[t,reg,seas,:], axis=-1)
            seas_daytemp_wrf11_sort = np.sort(seas_daytemp_wrf11[t,reg,seas,:], axis=-1)
            seas_daytemp_wrf44_sort = np.sort(seas_daytemp_wrf44[t,reg,seas,:], axis=-1)
            seas_daytemp_lucas_sort = np.sort(seas_daytemp_lucas[t,reg,seas,:], axis=-1)

            # find quantiles
            for i in range(19):
                quant[i] = (i+1)*(count[seas]+1)/20
                a[i] = int(quant[i])
                b[i] = modf(quant[i])[0]
        
                q_eobs[i] = seas_daytemp_eobs_sort[int(a[i])]+np.round(b[i],2)*(seas_daytemp_eobs_sort[int(a[i])+1]-seas_daytemp_eobs_sort[int(a[i])])
                q_wrf11[i] = seas_daytemp_wrf11_sort[int(a[i])]+np.round(b[i],2)*(seas_daytemp_wrf11_sort[int(a[i])+1]-seas_daytemp_wrf11_sort[int(a[i])])
                q_wrf44[i] = seas_daytemp_wrf44_sort[int(a[i])]+np.round(b[i],2)*(seas_daytemp_wrf44_sort[int(a[i])+1]-seas_daytemp_wrf44_sort[int(a[i])])
                q_lucas[i] = seas_daytemp_lucas_sort[int(a[i])]+np.round(b[i],2)*(seas_daytemp_lucas_sort[int(a[i])+1]-seas_daytemp_lucas_sort[int(a[i])])

                  
            # min limit
            xmin_w11 = seas_daytemp_wrf11_sort[0]#[quant+1]
            xmin_e = seas_daytemp_eobs_sort[0]#[quant+1]
            xmin_w44 = seas_daytemp_wrf44_sort[0]#[quant+1]
            xmin_lucas = seas_daytemp_lucas_sort[0]#[quant+1]
            xmin = np.nanmin([xmin_e,xmin_w11,xmin_w44,xmin_lucas])

            # max limit
            xmax_w11 = seas_daytemp_wrf11_sort[count[seas]-1]#[int(0.95*count[seas])+1]
            xmax_w44 = seas_daytemp_wrf44_sort[count[seas]-1]#[int(0.95*count[seas])+1]
            xmax_e = seas_daytemp_eobs_sort[count[seas]-1]#[int(0.95*count[seas])+1]
            xmax_lucas = seas_daytemp_lucas_sort[count[seas]-1]#[int(0.95*count_l[seas])+1]
            xmax = np.nanmax([xmax_e,xmax_w11,xmax_w44,xmax_lucas])
            
            print(xmin)
            print(xmax)

            ax[row,col].set_ylim(xmin-1,xmax+1)
            ax[row,col].set_xlim(xmin-1,xmax+1)
            loc1 = plticker.MultipleLocator(base=5) # this locator puts ticks at regular intervals
            ax[row,col].xaxis.set_major_locator(loc1)
            ax[row,col].yaxis.set_major_locator(loc1)
            ax[row,col].tick_params(axis='both', which='major', direction='in', labelsize=13)
            loc2 = plticker.MultipleLocator(base=1)  
            ax[row,col].xaxis.set_minor_locator(loc2)
            ax[row,col].yaxis.set_minor_locator(loc2)
            ax[row,col].tick_params(axis='both', which='minor', direction='in')

            # diagonal line
            line=np.linspace(xmin-5,xmax+5,10)
            ax[row,col].plot(line,line,color='black',linewidth=0.5)
            print('Plotting')
            

            # plot extremes
            ax[row,col].scatter(xmin_e, xmin_w11, marker='+', s=150, c='red')
            ax[row,col].scatter(xmax_e, xmax_w11, marker='+', s=150, c='red')
            # plot extremes
            ax[row,col].scatter(xmin_e, xmin_w44, marker='+', s=150, c='blue')
            ax[row,col].scatter(xmax_e, xmax_w44, marker='+', s=150, c='blue')
            # plot extremes
            ax[row,col].scatter(xmin_e, xmin_lucas, marker='+', s=150, c='green')
            ax[row,col].scatter(xmax_e, xmax_lucas, marker='+', s=150, c='green')
            # plot quantiles
            l1 = ax[row,col].scatter(q_eobs, q_wrf11, marker='+', s=150, c='red', label='WRF (0.11'+chr(176)+')')
            l2 = ax[row,col].scatter(q_eobs, q_wrf44, marker='+', s=150, c='blue', label='WRF (0.44'+chr(176)+')')
            l3 = ax[row,col].scatter(q_eobs, q_lucas, marker='+', s=150, c='green', label='LUCAS (0.44'+chr(176)+')')

            ax[row,col].set_xlabel('T('+chr(176)+'C) E-OBs', fontsize=20, labelpad=5)
            ax[row,col].set_ylabel('T('+chr(176)+'C) WRF', fontsize=20,  labelpad=5)
            ax[row,col].set_title( names[reg], fontsize=22, y=1.02)
                

        plt.figlegend((l1,l2,l3), ('EURO-CORDEX (0.11'+chr(176)+')', 'EURO-CORDEX (0.44'+chr(176)+')', 'LUCAS (0.44'+chr(176)+')'), loc='lower right', bbox_to_anchor=(0.82,0.15), fontsize=22)
        fig.suptitle('Q-Q plots\n' + seasons[seas]+ ' ' +temperatures[t] + ' 1990-2008', fontsize=25)
        plt.subplots_adjust( hspace=0.4, wspace=0.3)        
        plt.savefig('qq_subplots/vergina_qq_' + seasons[seas] + '_' + temp[t] + '.pdf', bbox_inches='tight')
        
        plt.clf()
        plt.close()
