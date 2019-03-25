'''
Created on Feb 17, 2017

@author: mike.sweet
'''

import datetime

import pytz

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
import plotly.plotly as pyplot
import plotly.tools as pytools
import plotly.graph_objs as go
# import plotly.offline as pyo

# pyplot user name
pyplotuser = 'mdsweet'
# PyPlot hash code
pyplotapikey = 'ddejj1kzPeisigzHeaw8'
# Color Brewer at http://colorbrewer2.org/#type=diverging&scheme=RdBu&n=5
# hex_colors = {'redish':'#ca0020', 'pinkish':'#f4a582','whitish':'#f7f7f7','ltbluish':'#92c5de','dkbluish':'#0571b0','blackish':'#A0A0A0'}
rgb_colors = {'redish':'rgb(202,0,32)', 'pinkish':'rgb(244,165,130)','whitish':'rgb(247,247,247)','ltbluish':'rgb(146,197,222)','dkbluish':'rgb(5,113,176)','blackish':'rgb(160,160,160)'}

LOCAL_TIME_ZONE = pytz.timezone("America/Denver")

# Color Brewer at http://colorbrewer2.org/#type=diverging&scheme=RdBu&n=5
colors = {'redish':'#ca0020', 'pinkish':'#f4a582','whitish':'#f7f7f7',
              'ltbluish':'#92c5de','dkbluish':'#0571b0'}

def UTCms_to_localstring(utcms):
    datetuple = datetime.datetime.utcfromtimestamp(utcms)
    local_dt = datetuple.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIME_ZONE)
    local_dtn = LOCAL_TIME_ZONE.normalize(local_dt) # .normalize might be unnecessary
    # Format: 2015-01-10 15:30:12 (required by Plotly
    datestr = local_dtn.strftime("%Y-%m-%d %H:%M")
    return datestr

def GraphTemperature(name,outpath,xlist,ylist):
    title = "Air Temperature" 
    pltcolor = rgb_colors['redish']
    ylabel = "Temperature (F)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphBatteryPer(name,outpath,xlist,ylist):
    title = "Battery Voltage" 
    pltcolor = rgb_colors['dkbluish']
    ylabel = "Voltage (percent)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphBatteryMV(name,outpath,xlist,ylist):
    title = "Battery Voltage" 
    pltcolor = rgb_colors['dkbluish']
    ylabel = "Voltage (millivolts)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSolarRad(name,outpath,xlist,ylist):
    title = "Solar Radiation" 
    pltcolor = rgb_colors['redish']
    ylabel = "Solar Radiation (watts-per-meter-sq)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphRelHumidity(name,outpath,xlist,ylist):
    title = "Relative Humidity" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Relative Humidity (percent)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphWindspeed(name,outpath,xlist,ylist):
    title = "Windspeed" 
    pltcolor = rgb_colors['pinkish']
    ylabel = "Windspeed (mph)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphWindGusts(name,outpath,xlist,ylist):
    title = "Wind Gusts" 
    pltcolor = rgb_colors['pinkish']
    ylabel = "Wind Gusts (mph)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphWindDirection(name,outpath,xlist,ylist):
    title = "Wind Direction" 
    pltcolor = rgb_colors['pinkish']
    ylabel = "Wind direction (degrees)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphDewpoint(name,outpath,xlist,ylist):
    title = "Dew Point" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Dew Point (F)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphPrecipitation(name,outpath,xlist,ylist):
    title = "Precipitation" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Precipitation (inches)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphPrecipTotal(name,outpath,xlist,ylist):
    title = "Daily Precipitation" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Daily Precipitation (inches)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphPressure(name,outpath,xlist,ylist):
    title = "Barometric Pressure" 
    pltcolor = rgb_colors['dkbluish']
    ylabel = "Barometric Pressure (inches)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphHitNumber(name,outpath,xlist,ylist):
    title = "Lightning Hits" 
    pltcolor = rgb_colors['redish']
    ylabel = "Lightning Hits (number)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphHitDistance(name,outpath,xlist,ylist):
    title = "Lightning Distance" 
    pltcolor = rgb_colors['redish']
    ylabel = "Lightning Distance (kilometers)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilTemp4(name,outpath,xlist,ylist):
    title = "4-inch Soil Temperature" 
    pltcolor = rgb_colors['redish']
    ylabel = "4-inch Soil Temperature (F)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilTemp8(name,outpath,xlist,ylist):
    title = "8-inch Soil Temperature" 
    pltcolor = rgb_colors['redish']
    ylabel = "8-inch Soil Temperature (F)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilTemp20(name,outpath,xlist,ylist):
    title = "20-inch Soil Temperature" 
    pltcolor = rgb_colors['redish']
    ylabel = "20-inch Soil Temperature (F)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilTemp36(name,outpath,xlist,ylist):
    title = "36-inch Soil Temperature" 
    pltcolor = rgb_colors['redish']
    ylabel = "36-inch Soil Temperature (F)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilVWC4(name,outpath,xlist,ylist):
    title = "4-inch Soil Volumetric Water Content" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Volumetric Water Content (percent)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilVWC8(name,outpath,xlist,ylist):
    title = "8-inch Soil Volumetric Water Content" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Volumetric Water Content (percent)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilVWC20(name,outpath,xlist,ylist):
    title = "20-inch Soil Volumetric Water Content" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Volumetric Water Content (percent)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilVWC36(name,outpath,xlist,ylist):
    title = "36-inch Soil Volumetric Water Content" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Volumetric Water Content (percent)"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilEC4(name,outpath,xlist,ylist):
    title = "4-inch Soil Saturation Extract Conductivity" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Saturation Extract EC [mS/cm]"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilEC8(name,outpath,xlist,ylist):
    title = "8-inch Soil Saturation Extract Conductivity" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Saturation Extract EC [mS/cm]"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilEC20(name,outpath,xlist,ylist):
    title = "20-inch Soil Saturation Extract Conductivity" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Saturation Extract EC [mS/cm]"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def GraphSoilEC36(name,outpath,xlist,ylist):
    title = "36-inch Soil Saturation Extract Conductivity" 
    pltcolor = rgb_colors['ltbluish']
    ylabel = "Saturation Extract EC [mS/cm]"
    station = name
    LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist)
    return

def LineGraph(title,pltcolor,ylabel,station,outpath,xlist,ylist):
    newx = []
    for x in xlist:
        newx.append(UTCms_to_localstring(x))
    xlist = newx
    pytools.set_credentials_file(username=pyplotuser, api_key=pyplotapikey)
    # py.sign_in(self.smapconfig.pyplotuser,self.smapconfig.pyplotapikey)
    # Configure graph figure
    # Create a trace
    trace1 = go.Scatter(x=xlist, y=ylist,mode = 'lines',name = title, line=dict(width=1.0,simplify=True,shape='spline',color=pltcolor))
    data = [trace1]
   
    bandxaxis = go.XAxis(
        title="Dates",
        range=[min(xlist),max(xlist)],
        # tick0=min(xlist),
        showgrid=True,
        showline=True,
        autotick=True,
        gridwidth=2,
        tickmode='Auto',
        # dtick="M1",
        # nticks=10,
        ticks='outside',
        ticklen=8,
        tickwidth=1,
        tickcolor='#000',
        tickformat='%m/%d',
        showticklabels=True,
        mirror=True,
        linewidth=2
       )

    bandyaxis = go.YAxis(
        title=ylabel,
        # range=[self.miny,self.maxy],
        gridwidth=2,
        tick0=0,
        showgrid=True,
        showline=True,
        autotick=True,
        tickmode='Auto',
        nticks=10,
        ticks='outside',
        ticklen=8,
        tickwidth=1,
        tickcolor='#000',
        tickformat='',
        showticklabels=True,
        mirror=True,
        linewidth=2
        )
   
    textblock =""

    layout = go.Layout(title= title + ' -- ' + station, width=800, height=600, 
                       xaxis=bandxaxis, yaxis=bandyaxis, 
                           annotations=go.Annotations([
                            go.Annotation(
                                x=0.0,
                                y=1.2,
                                showarrow=False,
                                text=textblock,
                                xref='paper',
                                yref='paper'
                            )]),
                       legend=dict(orientation="h", x=0.0,xanchor='left',y=1.1,yanchor='auto',traceorder='normal',
                       font=dict(family='sans-serif',size=11,color='#000'),
                       bgcolor='#E2E2E2',bordercolor='#FFFFFF',borderwidth=2))
    
    fig = go.Figure(data=data, layout=layout)
    pyplot.image.save_as(fig,filename=outpath)    
    return

