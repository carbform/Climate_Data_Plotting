# %% [markdown]
# ## Import all the required packages

# %%
import rioxarray as rio
import numpy as np
import xarray as xr
import proplot as plot
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# %% [markdown]
# ## Customize the Proplot package (optional)

# %%
plot.rc.reset()

# Font properties (self-explanatory)
plot.rc['font.weight']='bold'
plot.rc['font.size']=14

# Tick propreties (self-explanatory)
plot.rc['tick.labelsize']=14
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
plot.rc['label.size'] = 'medium'


# %% [markdown]
# ## Using xarray to load the climate data
#   
# For this example, we will be using the Gridded Rainfall Data from [Indian Meteorological Department (IMD)](https://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html) which is available as a netCDF (.nc ) file. NetCDF is the most commonly used file format to store gridded climate data which is also CF compliant. Download the .nc files from the given link : [Rainfall Data](https://www.imdpune.gov.in/Clim_Pred_LRF_New/Grided_Data_Download.html). 
#   
# + **After you've downloaded the multiple .nc files, put them all in a folder of your choice.**
# + **We will use xarray to read all the multiple files at once.**

# %%
#Opening multiple datasets using xarray's open_mfdataset command. To open a single nc file, you can use the xr.open_dataset() comamnd.

ds = xr.open_mfdataset('/media/carbform/Study/IMD_data/rain1by1/*.nc') 

#### Change the file name and folder accordingly ####
# Check the properties of the loaded dataset by printing the variable
ds



# %% [markdown]
# **This dataset has only variable: rf. We can access this variable simply by using ds.rf command**
# **The xarray package loads this as a Data Array which has three dimensions :**
# + Latitude (lat)
# + Longitude (lon)
# + Time (time)
# 
# **The picture below provides a useful visualization of how the gridded data is arranged**. For more info on how xarray works, click [here.](https://xarray.pydata.org/en/stable/)

# %%
ds.rf

# %% [markdown]
# **Checking the longitude, latitude and time dimensions in the loaded xarray dataset**

# %%
ds.lon


# %%
ds.lat

# %%
ds.time

# %% [markdown]
# ## Performing operations on the rainfall data

# %% [markdown]
# **First, we will slice/select the data according to our needs**
# + Selecting a specific date, **for example 1995-05-17**
# + Selecting a specific location (latitude and longitude): **Latitude : 18.5, Longitdue: 82.5**

# %% [markdown]
# **To perform operations on all the variables in the dataset, we can directly use the original dataset variable (ds).
# To perform operations on a specific variable, such as rainfall (rf), we can explicitly pass the variable name (ds.rf) before performing any operation.**
#  
# + In our case, since we have only one variable, we can also directly operate on **ds** without specifying the variable.
# + However, to be as general as possible, we will explicitly pass the **rainfall (ds.rf)** variable before performing any operation.

# %%
ds_sel_time = ds.rf.sel(time='1995-05-17T00:00:00.000000000') # time selection
ds_sel_loc = ds.rf.sel(lat=18.5,lon=82.5) # location selection

# %%
ds_sel_time # This is a 2-D array of rainfall values on that particular time value.

# %%
ds_sel_loc # This is 1-D time-series of rainfall values for that particular location.

# %% [markdown]
# **We can also use the isel() function to use indices to select and subset the data**
# + Selecting a specific date using the index (0): **for example the first time step which is 1901-01-01**
# + Selecting a specific location using the index (10,10)(latitude and longitude): **Latitude : 16.5, Longitdue: 76.5**

# %%
ds_sel_time_idx = ds.rf.isel(time=0) # time selection
ds_sel_loc_idx = ds.rf.isel(lat=10,lon=10) # location selection

# %%
ds_sel_time_idx # This is a 2-D array of rainfall values on that particular time value.

# %%
ds_sel_loc_idx # This is a 2-D array of rainfall values on that particular time value.

# %% [markdown]
# ## **Now, we will perform operations on the time axis of the rainfall dataset.**
# + Mean over time
# + Variance over time
# + Grouping over time
# + Resampling over time
# 
# P.S: These operations can be perorfmed along any dimension other than time.

# %%
# Mean and Variance of the data along the time axis.
ds_mean = ds.rf.mean('time')
ds_var = ds.rf.var('time')

# %%
ds_mean

# %%
ds_var

# %% [markdown]
# **We can also group the data along the time axis into either hours, days, months and years. The, we can apply methods such as mean and variance to the grouped dataset.**

# %%
ds_year=ds.groupby('time.year') # Also, we can use 'time.month',  'time.day' and 'time.dayofyear' for grouping.
ds_year_mean = ds_year.mean('time') 
ds_year_mean # Annual mean rainfall

# %% [markdown]
# **Using the 'time.dayofyear' argument to get the daily climatology of rainfall**

# %%
ds_daily_clim=ds.groupby('time.dayofyear').mean('time') # we get the mean of each day across all years
ds_daily_clim
# notice that the final dimensions are (lat,lon,dayofyear)

# %% [markdown]
# **We can use the resample function to sample our data at a different resolution.**

# %%
ds_res_month = ds.resample(time='1M') # Valid arguments are '1M'.'1D' and '1Y'.
# Then, we can apply mean, sum,variance etc.
ds_res_month.sum('time') # Monthly Rainfall Accumulation

# %% [markdown]
#  # Plotting the rainfall data

# %% [markdown]
# ## Default xarray plot commands (which use matplotlib) to generate plots.
# **Remember that we can only plot arrays upto 2 dimensions only.** 
# 
# **So, we can either select a slice of the original dataset or plot the 2-D arrays and 1-D time series that we generated earlier.**

# %%
ds.rf.sel(time='1995-08-31T00:00:00.000000000').plot() # extracting a specific time slice and plotting it.

# %%
ds_sel_time_idx.plot() # Same as above but here we directly load the variable that we extracted earlier.

# %%
ds_sel_loc_idx.plot()

# %% [markdown]
# ***Using the  globals() functions is to generate the variable names within a loop.***
# **We will be rquiring to call variables within a loop as follows : if a variable is stored as ds_clim, we can use 
# globals()['ds_clim'] to get the ds_clim variable**
# ***This command is very useful while plotting the data.***
# 

# %% [markdown]
# # Using the Proplot package to generate publication qualilty plots

# %% [markdown]
# **Matplotlib is an extremely versatile plotting package used by scientists and engineers far and wide. However, matplotlib can be cumbersome or repetitive for users who…**
# 
# + Make highly complex figures with many subplots.
# 
# + Want to finely tune their annotations and aesthetics.
# 
# + Need to make new figures nearly every day.
# 
# **More info on proplot can be found [here.](https://proplot.readthedocs.io/en/latest/index.html)**

# %%
# Generate the figure and axis with nrows and ncols for subplots ###
fig, axs=plot.subplots(ncols=2,nrows=1, proj='cyl',tight=True) 

##### proj = 'cyl' is the Cylindrical Equidistant Map projection used by Cartopy ###


lat_min = 6 # # Minimum latitude on the map
lat_max = 38 # Maximum latitude on the map
lon_min = 66 # # Minimum longitude on the map
lon_max = 98 # # Maximum longitude on the map

cm = 'jet' # Colormap 'rainbow' , 'viridis', 'RdYlBu', 'RdBu' etc..
ex= 'max' # Color bar arrow ,'min', 'max', 'none','both'

#Now, we can format all the axes at once using these commands

axs.format(lonlim=(lon_min, lon_max), 
           latlim=(lat_min, lat_max), 
           labels=True,
           innerborders=False, 
           latlines=10, lonlines=10,
           abc='(a)', abcloc='ll', 
           gridminor=False,
           suptitle='IMD Rainfall' )

######## Limits as above; ### labels = True for lat lon labels,
###### inner borders = False , If True, it will show rivers #####
###latlines=1, lonlines=1  spacing ########
#abc=False, It abc='(a)', it will automatically give subplot (a),(b),(c) etc....
####abcloc='ll', abc location
#### gridminor=False; if true it will show all gridlines of lat , lon

# Subtitles for each plot
# We can declare the subtitles now and use it further
title=['Mean Daily Rainfall','Daily Rainfall Variance' ]

# We can declare varaible names now and use it further
vars =['ds_mean','ds_var']
levels_mean= np.arange(0,11,1)  # generates a sequence of numbers from 0 to 10 with  a spacing of 1
levels_var= np.arange(30,160,10) 
levels =['levels_mean','levels_var'] # for indexing later
labels = ['mm/day','$(mm/day)^2$'] # for indexing later

###########Subplots ################ 

#contourf for contours

#pcolormesh for psuedo color plot

#Each subplot axis is numbered as axs[0] or axs[1] etc....]

# We can loop over each plot by indexing it as axs[i] where i is the indexing variable

for i in range(0,2): 
        #######################
        
        m=axs[i].pcolor(globals()[vars[i]], # globals() and vars[i] are used to index and generate the variable name
        cmap=cm, # Colormap
        transform=ccrs.PlateCarree(), # cartopy map projection
        extend=ex,  #colorbar style
        levels = globals()[levels[i]] # using globals to get levels variable
        )
        axs[i].format(title=title[i])
        axs[i].coastlines() # adds coastlines
        axs[i].colorbar(m,loc='r',drawedges=True, width = 0.10 , length=0.65, label=labels[i]) 

  

# Colorbar

#fig.colorbar will ive 1 common colorbar for all plots. But for common colorbar give explict levels.

#Use axs[i].colorbar for individual colorbars ########  

# axs[1].colorbar(n,loc='b',drawedges=True, width = 0.10 , length=0.65, label= 'Rainfall')


# %%
# Saving the figures
# Use the desired file extesnsion (jpg, eps, png, svg etc.)
fig.savefig('/home/carbform/Climate_Data_Plotting/plots/1.svg')


