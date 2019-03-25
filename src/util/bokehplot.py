#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 26, 2016

@author: mike.sweet
'''

from math import pi
import os

from bokeh.models import HoverTool
# from bokeh.models import DatetimeTickFormatter, HoverTool
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
# from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.formatters import TickFormatter, DatetimeTickFormatter

import pandas as pd
from bokeh.models.tickers import DaysTicker


# from bokeh.charts import segment, circle
def plot_temperature(df,cols,htmlpath,stationlbl,display):
    '''Plots line graph for air temperature

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    for col in cols:
        if col not in df.columns:
            return
    
    # Convert all value text to numeric data type
    for col in cols:
        df[col] = df[col].apply(pd.to_numeric, errors='coerce')

    # add a line renderer with legend and line thickness
    davislist = ['out_temp','hi_out_temp','low_out_temp']
        # add a line renderer with legend and line thickness
    decagonlist = ['Temp']

    colcount = 0
    for col in cols:
        if col == decagonlist[0]:
            df['AirTemp'] = df[col].apply(lambda x:((float(x)*1.8)+32.0) )
        colcount = df[col].count()

    for col in cols:
        if col == davislist[0]:
            df.ix[df[col]==3276.7,col]= None
            df['AirTemp'] = df[col].apply(lambda x:(float(x)))
        if col == davislist[1]:
            df.ix[df[col]==3276.7,col]= None
            df['HiTemp'] = df[col].apply(lambda x:(float(x)))
        if col == davislist[2]:
            df.ix[df[col]==-3276.7,col]= None
            df['LowTemp'] = df[col].apply(lambda x:(float(x)))
        colcount = colcount + df[col].count()
    
    if colcount == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # add a line renderer with legend and line thickness
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'AirTemp'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (air temperature, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Temperature (°F)',tools=TOOLS)
    
    if cols[0] in davislist:
        source = ColumnDataSource(data=dict(
            time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
            tavg=df['AirTemp'],
            tmin=df['LowTemp'],
            tmax=df['HiTemp'],
            ))
        
    if cols[0] in decagonlist:
        source = ColumnDataSource(data=dict(
            time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
            tavg=df['AirTemp'],
            ))
    
    # add a line renderer with legend and line thickness
    legenddict = {'AirTemp':"air",'HiTemp':"max",'LowTemp':"min"}
    p.line(df['Timestamp'], df['AirTemp'], color="#FF4F33", legend=legenddict['AirTemp'], line_width=2, source=source)
    # p.line(df['Timestamp'], df['HiTemp'], color="#FF4F33", legend=legenddict['HiTemp'], line_width=2, source=source)
    # p.line(df['Timestamp'], df['LowTemp'], color="#FF4F33", legend=legenddict['LowTemp'], line_width=2, source=source)

    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    
    if cols[0] in davislist:
        hover.tooltips = [("Min °F","@tmin{0.0}"),("Avg °F","@tavg{0.0}"),("Max °F","@tmax{0.0}"),("Date","@time")]
    if cols[0] in decagonlist:
        hover.tooltips = [("°F","$y{0.0}"),("Date","@time")]
   
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_precip(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for precipitation.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert from mm to inches for plotting (Decagon only)
    if col == 'Precip':
        df[col] = df[col].apply(lambda x:((float(x)*0.0393701)))
    if col == 'rainfall':
        df['Precip'] = df[col]
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'Precip'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (precipitation, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Precipitation (in)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        precip=df['Precip'],
        ))
    
    # add a line renderer with legend and line thickness
    # p.line(df['Timestamp'], df['Precip'], line_width=2, source=source)
    p.segment(x0=df['Timestamp'], y0=0, x1=df['Timestamp'],
              y1=df['Precip'], color="#3371FF",line_width=2)
    p.circle(df['Timestamp'], df['Precip'], size=4, color="#3371FF", alpha=1.0, source=source)
    
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("in","@precip{0.00}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_preciprate(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for precipitation.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    if col == 'hi_rain_rate':
        df['Precip'] = df[col]
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'PrecipRate'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (high precipitation rate, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Precipitation (inches per hour)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        precip=df['Precip'],
        ))
    
    # add a line renderer with legend and line thickness
    # p.line(df['Timestamp'], df['Precip'], line_width=2, source=source)
    p.segment(x0=df['Timestamp'], y0=0, x1=df['Timestamp'],
              y1=df['Precip'], color="#3371FF",line_width=2)
    p.circle(df['Timestamp'], df['Precip'], size=4, color="#3371FF", alpha=1.0, source=source)
    
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("in./hr.","@precip{0.00}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_soil_temp(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['soil_temp1','soil_temp2','soil_temp3']
        # add a line renderer with legend and line thickness
    decagonlist = ['SoilTemp4','SoilTemp8','SoilTemp20','SoilTemp36']

    if col in decagonlist:
        df['SoilTemp'] = df[col].apply(lambda x:((float(x)*1.8)+32.0) )
    if col in davislist:
        df.ix[df[col]==255,col]= None
        df['SoilTemp'] = df[col].apply(lambda x:(float(x)-90))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # add a line renderer with legend and line thickness
    extdict = {'SoilTemp4':'SoilTemp4','SoilTemp8':'SoilTemp8','SoilTemp20':'SoilTemp20',
                  'SoilTemp36':'SoilTemp36','soil_temp1':'SoilTemp6',
                  'soil_temp2':'SoilTemp18','soil_temp3':'SoilTemp36'}
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+extdict[col]+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (soil temperature, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Temperature (°F)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    legenddict = {'SoilTemp4':"4-inch depth",'SoilTemp8':"8-inch depth",'SoilTemp20':"20-inch depth",
                  'SoilTemp36':"36-inch depth",'soil_temp1':"6-inch depth",
                  'soil_temp2':"18-inch depth",'soil_temp3':"36-inch depth"}
    p.line(df['Timestamp'], df['SoilTemp'], color="#F4A582", legend=legenddict[col], line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("°F","$y{0.00}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_solar_rad(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['solar_rad']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['SolarRad'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==32767,col]= None
        df['SolarRad'] = df[col].apply(lambda x:(float(x)))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'SolarRad'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (solar radiation, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Solar Radiation (Watts/m2)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['SolarRad'], color="#F4A582", legend="solar radiation", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Watts/m2","$y{0.00}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_high_solar(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['high_solar_rad']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['HighSolar'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==32767,col]= None
        df['HighSolar'] = df[col].apply(lambda x:(float(x)))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'HighSolar'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (high solar radiation, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Solar Radiation (Watts/m2)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['HighSolar'], color="#F4A582", legend="solar radiation", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Watts/m2","$y{0.00}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_average_wind(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['avg_wind']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['AvgWind'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==255,col]= None
        df['AvgWind'] = df[col].apply(lambda x:(float(x)))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'AvgWind'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (average wind speed, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Average Wind Speed (MPH)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['AvgWind'], color="#F4A582", legend="average wind speed", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("MPH","$y{0}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_high_wind(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['hi_wind']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['HiWind'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==0,col]= None
        df['HiWind'] = df[col].apply(lambda x:(float(x)))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'HighWind'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (high wind speed, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='High Wind Speed (MPH)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['AvgWind'], color="#F4A582", legend="high wind speed", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("MPH","$y{0}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_evapo_trans(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['ET']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['ET'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==0,col]= None
        df['ET'] = df[col].apply(lambda x:(float(x)/1000))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'ET'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (evapotranspiration, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Evapotranspiration (in per hour)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['ET'], color="#F4A582", legend="evapotranspiration", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("in","$y{0.000}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_avg_uv(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['avg_UV']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['AvgUV'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==255,col]= None
        df['AvgUV'] = df[col].apply(lambda x:(float(x)/10))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'AvgUV'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (average UV, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Average UV index',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['AvgUV'], color="#F4A582", legend="average UV index", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("UV","$y{0.0}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_humidity(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['out_humidity']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['Humidity'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==2.55,col]= None
        df['Humidity'] = df[col].apply(lambda x:(float(x)*100.0))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'Humidity'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (humidity, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Humidity (%)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['Humidity'], color="#3371FF", legend="humidity", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("%","$y{0}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_barometer(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['barometer']
        # add a line renderer with legend and line thickness
    decagonlist = []

    if col in decagonlist:
        df['Barometer'] = df[col].apply(lambda x:(float(x)))
    if col in davislist:
        df.ix[df[col]==0,col]= None
        df['Barometer'] = df[col].apply(lambda x:(float(x)))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+'Barometer'+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (barometric pressure, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Barometric pressure (in)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    p.line(df['Timestamp'], df['Barometer'], color="#3371FF", legend="barometric pressure", line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("in.","$y{0}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_soil_moisture(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Convert Celsius to Fahrenheit for plotting

    # add a line renderer with legend and line thickness
    davislist = ['soil_moist1','soil_moist2','soil_moist3']
        # add a line renderer with legend and line thickness
    decagonlist = ['SoilMoist4','SoilMoist8','SoilMoist20','SoilMoist36']

    if col in decagonlist:
        df['SoilMoist'] = df[col].apply(lambda x:((float(x)*1.8)+32.0) )
    if col in davislist:
        df.ix[df[col]==255,col]= None
        df['SoilMoist'] = df[col].apply(lambda x:(float(x)))

    if df[col].count() == 0:
        return
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # add a line renderer with legend and line thickness
    extdict = {'SoilMoist4':'SoilMoist4','SoilMoist8':'SoilMoist8','SoilMoist20':'SoilMoist20',
                  'SoilMoist36':'SoilMoist36','soil_moist1':'SoilMoist6',
                  'soil_moist2':'SoilMoist18','soil_moist3':'SoilMoist36'}
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+extdict[col]+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (soil moisture, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Pressure (centibars)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    legenddict = {'SoilMoist4':"4-inch depth",'SoilMoist8':"8-inch depth",'SoilMoist20':"20-inch depth",
                  'SoilMoist36':"36-inch depth",'soil_moist1':"6-inch depth",
                  'soil_moist2':"18-inch depth",'soil_moist3':"36-inch depth"}
    p.line(df['Timestamp'], df['SoilMoist'], color="#3371FF", legend=legenddict[col], line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("centibars","$y{0.0}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_elec_cond(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Numeric conversion if needed
    df['EC'] = df[col].apply(lambda x:(x) )
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+col+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (electrical conductivity, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Electrical Conductivity (mS/cm)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    legenddict = {'EC4':"4-inch depth",'EC8':"8-inch depth",'EC20':"20-inch depth",
                  'EC36':"36-inch depth"}
    p.line(df['Timestamp'], df['EC'], color="#DA33FF", legend=legenddict[col], line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("mS/cm","$y{0.000}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)

    return

def plot_vol_water_content(df,col,htmlpath,stationlbl,display):
    '''Plots line graph for given soil depth.

    Parameters
    ----------
    df:         Pandas data frame
    col:        Pandas column name 
    htmlpath:   Path to HTML output file
    stationlbl: Station label to appear in graph
    display:    Binary to determine if plot is displayed
    
    Returns
    -------
    None
      
    '''
    if col not in df.columns:
        return
    
    # Convert all value text to numeric data type
    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    # Numeric conversion if needed
    df['VWC'] = df[col].apply(lambda x:(x) )
    
    #=========================================================================
    # PLOTTING
    #=========================================================================
    
    # output to static HTML file
    # Valid path for OS
    htmlfile = os.path.normpath(htmlpath)
    head, tail = os.path.split(htmlfile)
    fname = os.path.splitext(tail)
    htmlfile = os.path.normpath(os.path.join(head,fname[0]+col+fname[1]))

    try:
        os.remove(htmlfile)
    except OSError:
        pass
    title = "Soil Moisture Station " + stationlbl + " (volumetric water content, raw values)"
    output_file(htmlfile,title=title,mode="cdn")
    
    # create a new plot with a title and axis labels
    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize,hover"
    p = figure(title=title,x_axis_label='Date', y_axis_label='Volumetric Water Content (m³/m³)',tools=TOOLS)
    
    source = ColumnDataSource(data=dict(
        time=df['Timestamp'].map(lambda x: x.strftime('%d-%b-%Y %I:%M %p')),
        ))
    
    # add a line renderer with legend and line thickness
    legenddict = {'VWC4':"4-inch depth",'VWC8':"8-inch depth",'VWC20':"20-inch depth",
                  'VWC36':"36-inch depth"}
    p.line(df['Timestamp'], df['VWC'], color="#3371FF", legend=legenddict[col], line_width=2, source=source)
    p.legend.location = "bottom_right"
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
            hours=["%d %b %Y"],
            days=["%d %b %Y"],
            months=["%d %b %Y"],
            years=["%d %b %Y"],
        ))
    
    #slant axis
    p.xaxis.major_label_orientation = pi/4
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("m³/m³","$y{0.000}"),("Date","@time")]
    
    save(p)
    # show the results
    if display:
        show(p)   
    return

'''
def linked_soil():
    #http://bebi103.caltech.edu/2015/tutorials/r1_intro_to_bokeh.html
    # Unmelt the DataFrame
    df_fish_unmelt = df_fish.pivot_table(index=['zeit', 'light', 'day', 'CLOCK'], 
                        columns='fish', values='activity').reset_index()
    
    # Creat data source
    source = bokeh.plotting.ColumnDataSource(df_fish_unmelt)
    
    # Determine when nights start and end
    lefts, rights = nights(df_fish[df_fish.fish=='FISH1'])
    
    # Create figures
    ps = [bokeh.plotting.figure(background_fill='#DFDFE5', plot_width=650, 
                                plot_height=250) for i in range(3)] 
    
    # Link ranges (enable linked panning/zooming)
    for i in (1, 2):
        ps[1].x_range = ps[0].x_range
        ps[2].x_range = ps[0].x_range
        ps[1].y_range = ps[0].y_range
        ps[2].y_range = ps[0].y_range
        
    # Label the axes
    for i in range(3):
        ps[i].yaxis.axis_label = 'sec of activity / 10 min'
        ps[i].xaxis.axis_label = 'time (h)'
    
    # Specify colors
    colors = ['dodgerblue', 'tomato', 'indigo']
    
    # Stylize
    for i, _ in enumerate(ps): 
        ps[i].xgrid.grid_line_color='white'
        ps[i].ygrid.grid_line_color='white'
        
    # Populate glyphs
    for i, fish in enumerate(['FISH11', 'FISH12', 'FISH23']):
        # Put in line
        ps[i].line(x='zeit', y=fish, line_width=1, source=source,
                   color=colors[i])
        
        # Label with title
        ps[i].title = fish
            
        # Make shaded boxes for nights
        night_boxes = []
        for j, left in enumerate(lefts):
            night_boxes.append(
                    bokeh.models.BoxAnnotation(plot=ps[i], left=left, right=rights[j], 
                                               fill_alpha=0.3, fill_color='gray'))
        ps[i].renderers.extend(night_boxes)
            
    my_plot = bokeh.plotting.vplot(*tuple(ps))
            
    bokeh.io.show(my_plot)
    return
    '''