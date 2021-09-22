#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 19:03:54 2021

@author: sarat
"""
##### Load packages #######
import rioxarray as rio
import numpy as np
import datetime as dt
import xarray as xr
import proplot as plot
import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import imdlib as imd
import statsmodels.api as sm
import matplotlib.dates as mdates
import cftime
import scipy.fft as fft
import seaborn as sns
import matplotlib.pyplot as plt
#%% plot properties #### fuck out and find out ######
plot.rc.reset()
# plot.register_fonts('/home/sarat/anaconda3/pkgs/proplot-0.8.1-pyhd8ed1ab_0/site-packages/proplot/fonts/Simplex.ttf')
# plot.register_fonts('/home/sarat/anaconda3/pkgs/proplot-0.8.1-pyhd8ed1ab_0/site-packages/proplot/fonts/ibm.ttf')
# plot.register_fonts('/home/sarat/anaconda3/pkgs/proplot-0.8.1-pyhd8ed1ab_0/site-packages/proplot/fonts/simpl_bold.ttf')
plot.register_fonts('/home/sarat/anaconda3/pkgs/proplot-0.8.1-pyhd8ed1ab_0/site-packages/proplot/fonts/IBMPlexSans-SemiBold.ttf')
plot.rc['font.name'] = 'IBM Plex Sans'
plot.rc['font.weight']='bold'
plot.rc['font.size']=10
plot.rc['tick.labelsize']=10

# plot.rc['xtick.minor.visible']     =   False
# plot.rc['ytick.minor.visible']     =   False
plot.rc['tick.len']=2
plot.rc['meta.width']=1.5
plot.rc['subplots.tight']= True
plot.rc['grid']=True
plot.rc['grid.linewidth']=0.25
plot.rc['grid.linestyle']=(0, (5, 10))
plot.rc['tick.dir']= 'out'

# plot.rc['colorbar.insetpad']='0.5em'
plot.rc['xtick.major.size']=3
plot.rc['ytick.major.size']=3

#%% Open the datset #### Change the file name and folder accordingly
ds1 = xr.open_dataset('/media/sarat/Study/SPI_India/nclimgrid_lowres_spi_gamma_01.nc')
ds2 = xr.open_dataset('/media/sarat/Study/SPI_India/nclimgrid_lowres_spi_gamma_03.nc')
ds3 = xr.open_dataset('/media/sarat/Study/SPI_India/nclimgrid_lowres_spi_pearson_01.nc')
ds4 = xr.open_dataset('/media/sarat/Study/SPI_India/nclimgrid_lowres_spi_pearson_03.nc')
ds_spi1 = ds1.spi_gamma_01 # Variable name here ###
ds_spi2 = ds2.spi_gamma_03 # Variable name here ###
############
ds_spi3=ds3.where(ds3>-3.08)
ds_spi4=ds4.where(ds4>-3.08)
ds_spi3 = ds3.spi_pearson_01# Variable name here ###
ds_spi4 = ds4.spi_pearson_03 # Variable name here ###
#%% Plotting Starts %%%%%%%%

#### Shapefile load #####
fname='/media/sarat/Study/india_administrative_state_boundary/FREE-INDIA-Shape-File/UNITED INDIA Shape File/United India.shp'
fname2='/media/sarat/Study/Bundelkhand/shape/bundelkhand.shp'
#### Figure starts ######
fig, axs=plot.subplots(ncols=2,nrows=1, proj='cyl', dpi=300,
                       tight=True) ### nrows and ncols for subplots ###
##### proj = 'cyl' Dont change ###
#### dpi = 300 ( recommended ) , 600 , 1200 
#### lata and lon limits #####
lat_min = 6 # Change accordingly now for India
lat_max = 38 # lat max
lon_min = 66 ###
lon_max = 98
levels=np.arange(-3,3,0.3) ### or  if we want our spacing ==> 
###############for example ### levels = [0,0.1,0.2]
cm = 'RdYlBu' # Colormap 'rainbow' , 'viridis', 'RdYlBu', 'RdBu' etc..
ex='both'  # Color bar arrow ,'left', 'right', 'none'
####################################
################################
axs.format(
        lonlim=(lon_min, lon_max), latlim=(lat_min, lat_max), labels=True,
        innerborders=False, latlines=4, lonlines=2,
        abc='(a)', abcloc='ll', gridminor=False,
     suptitle='SPI Demo' )
######## Limits as above; ### labels = True for lat lon labels,
###### inner borders = False , If True, it will show rivers #####
###latlines=1, lonlines=1  spacing ########
#abc=False, It abc='(a)', it will automatically give subplot (a),(b),(c) etc....
####abcloc='ll', abc location
#### gridminor=False; if true it will show all gridline of lat , lon
    
    #####################################################
   ######## Subplots ############# ### contourf for contours
   #### pcolormesh for pixel coloes ####
######################### Each subplot axis is numbered as axs[0] or axs[1] etc....]
m=axs[0].contourf(ds_spi1.isel(time=100),
                    cmap=cm,  extend=ex, 
                     
                        transform=ccrs.PlateCarree(), levels=levels )
#### adding shapefile ######
axs[0].add_geometries(Reader(fname).geometries(),
                      ccrs.PlateCarree(),facecolor='None',edgecolor='black', 
                      linewidth=1)
axs[0].format(title='1 Month')
###### Colorbar  fig.colorbar will ive 1 common colorbar for all plots#####
######### But for common colorbar give explict levels ######
####### Use axs[0].colorbar for individual colorbars ########    
# axs[0].colorbar(m,loc='b',drawedges=True, width = 0.10 , length=0.65, label='SPI-Gamma-1')
#############################################################
n=axs[1].pcolormesh(ds_spi2.isel(time=100),
                    cmap=cm,  extend=ex, 
                     
                        transform=ccrs.PlateCarree(), levels=levels )
#### adding shapefile ######
axs[1].add_geometries(Reader(fname).geometries(),
                      ccrs.PlateCarree(),facecolor='none',edgecolor='black', 
                      linewidth=1)
######### If face color given #### It will be opaque #####
####### This is for adding a new shapefile as overlay ######
# axs[1].add_geometries(Reader(fname2).geometries(),
#                       ccrs.PlateCarree(),facecolor='red',edgecolor='black', 
#                       linewidth=1)
axs[1].format(title='3 Month')
##########################
fig.colorbar(m,loc='b',drawedges=True, width = 0.10 , length=0.85, label='SPI-Gamma')
###### Colorbar  fig.colorbar will ive 1 common colorbar for all plots#####
######### But for common colorbar give explict levels ######
####### Use axs[0].colorbar for individual colorbars ########    
# axs[1].colorbar(n,loc='b',drawedges=True, width = 0.10 , length=0.65, label= 'SPI-Gamma- 3')
##########################################################################
 #%%###### 
   #### Pearson ##########
   ############################

# p=axs[2].pcolormesh(ds_spi3.isel(time=100),
#                     cmap=cm,  extend=ex,
                     
#                         transform=ccrs.PlateCarree(), levels=levels )
# #### adding shapefile ######
# axs[2].add_geometries(Reader(fname).geometries(),
#                       ccrs.PlateCarree(),facecolor='None',edgecolor='black', 
#                       linewidth=1)
# ###### Colorbar  fig.colorbar will ive 1 common colorbar for all plots#####
# ######### But for common colorbar give explict levels ######
# ####### Use axs[0].colorbar for individual colorbars ########    
# # axs[2].colorbar(p,loc='b',drawedges=True, width = 0.10 , length=0.65, label= 'SPI-Pearson -1')
# ###########################################################################
# q=axs[3].pcolormesh(ds_spi4.isel(time=100),
#                     cmap=cm,  extend=ex,
                     
#                         transform=ccrs.PlateCarree(), levels=levels )
# #### adding shapefile ######
# axs[3].add_geometries(Reader(fname).geometries(),
#                       ccrs.PlateCarree(),facecolor='None',edgecolor='black', 
#                       linewidth=1)
# ###### Colorbar  fig.colorbar will ive 1 common colorbar for all plots#####
# ######### But for common colorbar give explict levels ######
# ####### Use axs[0].colorbar for individual colorbars ########    
# # axs[3].colorbar(q,loc='b',drawedges=True, width = 0.10 , length=0.65, label= 'SPI-Pearson -3')
##################################################
######%%
#%% Saving figures ####
fig.savefig('/media/sarat/Study/Plots/eps/spi_ind1deg.eps')
fig.savefig('/media/sarat/Study/Plots/pdf/spi_ind1deg.pdf')