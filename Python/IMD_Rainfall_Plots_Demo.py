#!/usr/bin/env python
# coding: utf-8

# ## Import all the required packages

# In[30]:


import rioxarray as rio
import numpy as np
import xarray as xr
import proplot as plot
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


# ## Customize the Proplot package (optional)

# In[31]:


plot.rc.reset()

# Font properties (self-explanatory)
plot.register_fonts('/home/sarat/anaconda3/pkgs/proplot-0.8.1-pyhd8ed1ab_0/site-packages/proplot/fonts/IBMPlexSans-SemiBold.ttf')
plot.rc['font.name'] = 'IBM Plex Sans'
plot.rc['font.weight']='bold'
plot.rc['font.size']=10

# Tick propreties (self-explanatory)
plot.rc['tick.labelsize']=10
plot.rc['xtick.minor.visible'] =   False
plot.rc['ytick.minor.visible']=   False
plot.rc['tick.len']=2
plot.rc['tick.dir']= 'out'
plot.rc['xtick.major.size']=3
plot.rc['ytick.major.size']=3

# Grid properties (self-explanatory)
plot.rc['grid']=False
plot.rc['grid.linewidth']=0.25
plot.rc['grid.linestyle']=(0, (5, 10))

# Misc
plot.rc['meta.width']=1.5 # Line width in the plots
plot.rc['subplots.tight']= True # Tight layout for the subplots
plot.rc['colorbar.insetpad']='0.5em' # Insert whitespace around the colorbar


# ## Using xarray to load the climate data
#   
# For this example, we will be using the Gridded Rainfall Data from [Indian Meteorological Department (IMD)](https://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html) which is available as a netCDF (.nc ) file. NetCDF is the most commonly used file format to store gridded climate data which is also CF compliant. Download the .nc files from the given link : [Rainfall Data](https://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html). 
#   
# + **After you've downloaded the multiple .nc files, put them all in a folder of your choice.**
# + **We will use xarray to read all the multiple files at once.**

# In[32]:


#Opening multiple datasets using xarray's open_mfdataset command. 

ds = xr.open_mfdataset('/media/sarat/Study/IMD_data/rain1by1/*.nc') 

#### Change the file name and folder accordingly ####


# ## Check the properties of the loaded dataset

# In[33]:


ds


# **This dataset has only variable: rf. We can access this variable simply by using ds.rf command**
# **The xarray package loads this as a Data Array which has three dimensions :**
# + Latitude (lat)
# + Longitude (lon)
# + Time (time)
# 
# **The picture below provides a useful visualization of how the gridded data is arranged**. For more info on how xarray works, click [here.](https://xarray.pydata.org/en/stable/)

# In[34]:


ds.rf


# **Checking the longitude, latitude and time dimensions in the loaded xarray dataset**

# In[35]:



ds.lon


# In[36]:


ds.lat


# In[37]:


ds.time


# ## Performing operations on the rainfall data

# **First, we will slice/select the data according to our needs**
# + Selecting a specific date, **for example 1995-05-17**
# + Selecting a specific location (latitude and longitude): **Latitude : 18.5, Longitdue: 82.5**

# **To perform operations on all the variables in the dataset, we can directly use the original dataset variable (ds).
# To perform operations on a specific variable, such as rainfall (rf), we can explicitly pass the variable name (ds.rf) before performing any operation.**
#  
# + In our case, since we have only one variable, we can also directly operate on **ds** without specifying the variable.
# + However, to be as general as possible, we will explicitly pass the **rainfall (ds.rf)** variable before performing any operatiom.

# In[38]:


ds_sel_time = ds.rf.sel(time='1995-05-17T00:00:00.000000000') 
ds_sel_loc = ds.rf.sel(lat=18.5,lon=82.5) 


# In[39]:


ds_sel_time # This is a 2-D array of rainfall values on that particular time value.


# In[40]:


ds_sel_loc # This is 1-D time-series of rainfall values for that particular location.


# ## **Now, we will perform operations on the time axis of the rainfall dataset.**
# + Mean over time
# + Variance over time
# + Grouping over time
# + Resampling over time
# 
# These operations can be perorfmed along any dimension other than time.

# In[41]:


# Mean and Variance of the data along the time axis.
ds_mean = ds.rf.mean('time')
ds_var = ds.rf.var('time')


# In[42]:


ds_mean


# In[43]:


ds_var


# **We can also group the data along the time axis into either hours, days, months and years. The, we can apply methods such as mean and variance to the grouped dataset.**

# In[44]:


ds_year=ds.groupby('time.year') # Also, we can use 'time.month' and 'time.day' for grouping.
ds_year_mean = ds_year.mean('time') 
ds_year_mean # Annual mean rainfall


# **We can use the resample function to sample our data at a different resolution.**

# In[45]:


ds_res_month = ds.resample(time='1M') # Valid arguments are '1M'.'1D' and '1Y'.
# Then, we can apply mean, sum,variance etc.
ds_res_month.sum('time') # Monthly Rainfall Accumulation


#  # Plotting the rainfall data

# ## Default xarray plot commands (which use matplotlib) to generate plots.
# **Remember that we can only plot arrays upto 2 dimensions only.** 
# 
# **So, we can either select a slice of the original dataset or plot the 2-D arrays and 1-D time series that we generated earlier.**

# In[46]:


ds.rf.sel(time='1995-08-31T00:00:00.000000000').plot() # extracting a specific time slice and plotting it.


# In[47]:


ds_sel_time.plot() # Same as above but here we directly load the variable that we extracted earlier.


# In[48]:


ds_sel_loc.plot()


# # Using the Proplot package to generate publication qualilty plots

# **Matplotlib is an extremely versatile plotting package used by scientists and engineers far and wide. However, matplotlib can be cumbersome or repetitive for users who…**
# 
# + Make highly complex figures with many subplots.
# 
# + Want to finely tune their annotations and aesthetics.
# 
# + Need to make new figures nearly every day.
# 
# **More info on proplot can be found [here.](https://proplot.readthedocs.io/en/latest/index.html)**

# In[49]:


# Generate the figure and axis with nrows and ncols for subplots ###
fig, axs=plot.subplots(ncols=2,nrows=1, proj='cyl', dpi=300,
                       tight=True) 

##### proj = 'cyl' is the Cylindrical Equidistant Map projection used by Cartopy ###
#### dpi = 300 ( recommended ) , 600 , 1200 

lat_min = 6 # Change accordingly
lat_max = 38 # lat max
lon_min = 66 ###
lon_max = 98
levels=np.arange(0,10,1) # generates a sequence of numbers from 0 to 10 with  a spacing of 1
cm = 'RdYlBu' # Colormap 'rainbow' , 'viridis', 'RdYlBu', 'RdBu' etc..
ex= 'max' # Color bar arrow ,'min', 'max', 'none','both'

#Now, we can format all the axes at once using these commands

axs.format(lonlim=(lon_min, lon_max), 
           latlim=(lat_min, lat_max), 
           labels=True,
           innerborders=False, 
           latlines=4, lonlines=4,
           abc='(a)', abcloc='ll', 
           gridminor=False,
           suptitle='IMD Rainfall' )

######## Limits as above; ### labels = True for lat lon labels,
###### inner borders = False , If True, it will show rivers #####
###latlines=1, lonlines=1  spacing ########
#abc=False, It abc='(a)', it will automatically give subplot (a),(b),(c) etc....
####abcloc='ll', abc location
#### gridminor=False; if true it will show all gridlines of lat , lon


###########Subplots ################ 

#contourf for contours

#pcolormesh for psuedo color plot

#Each subplot axis is numbered as axs[0] or axs[1] etc....]

# 1st subplot

m=axs[0].contourf(ds_mean,     # Data to be plotted
                    cmap=cm,  # Colormap
                  extend=ex, 
                 transform=ccrs.PlateCarree(), # cartopy map projection
                  levels=levels )

axs[0].format(title='Mean Rainfall Contour')


# 2nd subplot

n=axs[1].pcolormesh(ds_mean,
                    cmap=cm,  
                    extend=ex, 
                    transform=ccrs.PlateCarree(), 
                    levels=levels )

axs[1].format(title='Mean Rainfall Pcolormesh')

# Colorbar

fig.colorbar(m,loc='b',drawedges=True, width = 0.10 , length=0.45, label='mm/day')

#fig.colorbar will ive 1 common colorbar for all plots. But for common colorbar give explict levels.

#Use axs[0].colorbar for individual colorbars ########    

# axs[1].colorbar(n,loc='b',drawedges=True, width = 0.10 , length=0.65, label= 'Rainfall')

