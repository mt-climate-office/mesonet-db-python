'''
Created on Feb 17, 2017

@author: mike.sweet
'''

import datetime

import pytz

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd


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
    # datestr = local_dtn.strftime('%d %B %Y %H:%M')
    datestr = local_dtn.strftime('%m/%d')
    return datestr

def UTCms_to_localstring2(utcms):
    datetuple = datetime.datetime.utcfromtimestamp(utcms)
    local_dt = datetuple.replace(tzinfo=pytz.utc).astimezone(LOCAL_TIME_ZONE)
    local_dtn = LOCAL_TIME_ZONE.normalize(local_dt) # .normalize might be unnecessary
    # Format: 2015-01-10 15:30:12 (required by Plotly
    datestr = local_dtn.strftime("%Y-%m-%d %H:%M")
    return datestr

def graph_getx(eledict):
    x = eledict['timestamp']
    return x

def graph_gety(eledict):
    y = eledict['values']
    return y

def graph_getfigure():
    fig = plt.figure(num=None, figsize=(4, 3), dpi=100, facecolor='w', edgecolor='k')
    return fig


def GraphBatteryPer(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.plot( x, y, color=colors['dkbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Battery Percent' )
    plt.ylim(0,110)
    ax.locator_params(nbins=10, axis='y')
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True
    
def GraphBatteryMV(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.plot( x, y, color=colors['dkbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Battery Millivolts' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSolarRad(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.plot( x, y, color=colors['redish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Solar Radiation' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphTemperature(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.plot( x, y, color=colors['redish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Temperature' )
    ax.locator_params(nbins=10, axis='y')
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphRelHumidity(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Relative Humidity (%)' )
    ax.locator_params(nbins=10, axis='y')
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphDewpoint(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Dew Point (F)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphWindspeed(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['pinkish'], marker='o')
    # plt.plot( x, y, color=colors['pinkish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Windspeed (mph)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphWindGusts(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['pinkish'], marker='o')
    # plt.plot( x, y, color=colors['pinkish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Wind gust (mph)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphWindDirection(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    plt.scatter( x, y, color=colors['pinkish'], marker='o')
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Wind direction (degrees)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphPrecipitation(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    # Eliminate values = 0.0 from plotting
    y1 = [n if n > 0.0 else np.NaN for n in y]
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # plt.vlines(x,[0],y1,color=colors['ltbluish'],linestyles='solid',linewidth=1.0, zorder=2)
    plt.scatter( x, y, color=colors['dkbluish'],alpha=0.0, marker='o', zorder=1)
    plt.scatter( x, y1, color=colors['dkbluish'], s=1.5, alpha=1.0, marker='o', zorder=3)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    # Set y-axis limits and label
    plt.ylabel( 'Precipitation (in.)' )
    plt.ylim(bottom=0.000)
    #----------
    # ADD "NO PRECIPITATION" across plot if y list is all nan
    if not sum(y) > 0.0:
        plt.text(0.5, 0.5,'no precipitation', horizontalalignment='center',
                 verticalalignment='center',transform=ax.transAxes)
    #----------
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    ax.set_xticklabels(labels, rotation=45)
    # lims = plt.xlim()
    # print plt.xlim(lims[0],lims[1])
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphPrecipTotal(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    # Eliminate values = 0.0 from plotting
    y1 = [n if n > 0.0 else np.NaN for n in y]
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # plt.vlines(x,[0],y1,color=colors['ltbluish'],linestyles='solid',linewidth=1.0, zorder=2)
    plt.scatter( x, y, color=colors['dkbluish'],alpha=0.0, marker='o', zorder=1)
    plt.scatter( x, y1, color=colors['dkbluish'], s=1.5, alpha=1.0, marker='o', zorder=3)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    # Set y-axis limits and label
    plt.ylabel( 'Precipitation (in.)' )
    plt.ylim(bottom=0.000)
    #----------
    # ADD "NO PRECIPITATION" across plot if y list is all nan
    if not sum(y) > 0.0:
        plt.text(0.5, 0.5,'no precipitation', horizontalalignment='center',
                 verticalalignment='center',transform=ax.transAxes)
    #----------
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    ax.set_xticklabels(labels, rotation=45)
    # lims = plt.xlim()
    # print plt.xlim(lims[0],lims[1])
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphHitNumber(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    # Eliminate values = 0.0 from plotting
    y1 = [n if n > 0.0 else np.NaN for n in y]
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # plt.vlines(x,[0],y1,color=colors['pinkish'],linestyles='solid',linewidth=1.0, zorder=2)
    plt.scatter( x, y, color=colors['redish'],alpha=0.0, marker='o', zorder=1)
    plt.scatter( x, y1, color=colors['redish'], s=1.5, alpha=1.0, marker='o', zorder=3)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    # Set y-axis limits and label
    plt.ylabel( 'Lightning Strikes' )
    plt.ylim(bottom=0.000)
    #----------
    # ADD "NO PRECIPITATION" across plot if y list is all nan
    if not sum(y) > 0.0:
        plt.text(0.5, 0.5,'no lightning strikes', horizontalalignment='center',
                 verticalalignment='center',transform=ax.transAxes)
    #----------
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    ax.set_xticklabels(labels, rotation=45)
    # lims = plt.xlim()
    # print plt.xlim(lims[0],lims[1])
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphHitDistance(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    # Eliminate values = 0.0 from plotting
    y1 = [n if n > 0.0 else np.NaN for n in y]
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # plt.vlines(x,[0],y1,color=colors['pinkish'],linestyles='solid',linewidth=1.0, zorder=2)
    plt.scatter( x, y, color=colors['redish'],alpha=0.0, marker='o', zorder=1)
    plt.scatter( x, y1, color=colors['redish'], s=1.5, alpha=1.0, marker='o', zorder=3)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    # Set y-axis limits and label
    plt.ylabel( 'Distance (km.)' )
    plt.ylim(bottom=0.000)
    #----------
    # ADD "NO PRECIPITATION" across plot if y list is all nan
    if not sum(y) > 0.0:
        plt.text(0.5, 0.5,'no lightning strikes', horizontalalignment='center',
                 verticalalignment='center',transform=ax.transAxes)
    #----------
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    ax.set_xticklabels(labels, rotation=45)
    # lims = plt.xlim()
    # print plt.xlim(lims[0],lims[1])
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphPressure(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['dkbluish'], marker='o', s=2)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # Set y-axis limits and label
    plt.ylabel( 'Barometric Pressure (in)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilTemp4(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['redish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['redish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # plt.ticklabel_format(useOffset=False, style='plain')
    # ax.get_xaxis().get_major_formatter().set_scientific(False)
    # ax.get_yaxis().get_major_formatter().set_scientific(False)
    # Set y-axis limits and label
    plt.ylabel( '4-inch Soil Temperature (F)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(bottom=int(min(y)),top=int(max(y)))
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilTemp8(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['redish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['redish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # plt.ticklabel_format(useOffset=False, style='plain')
    # ax.get_xaxis().get_major_formatter().set_scientific(False)
    # ax.get_yaxis().get_major_formatter().set_scientific(False)
    # Set y-axis limits and label
    plt.ylabel( '8-inch Soil Temperature (F)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(bottom=int(min(y)),top=int(max(y)))
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilTemp20(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    try:
        x = xlist
        y = ylist
        fig = graph_getfigure()
        ax = fig.add_subplot(111)
        # Plot data
        plt.scatter( x, y, color=colors['redish'], marker='o', s=2)
        # plt.plot( x, y, color=colors['redish'], linewidth=2.0)
        # Set x-axis data labels
        plt.xlabel( 'Date' )
        locs = plt.xticks()[0]
        labels = [item.get_text() for item in ax.get_xticklabels()]
        loclen = len(locs)
        for k in range(0,loclen):
            labels[k] = UTCms_to_localstring(int(locs[k]))
        ax.set_xticklabels(labels, rotation=45)
        # ax.yaxis.get_major_formatter().set_scientific(False)
        # ax.yaxis.get_major_formatter().set_useOffset(False)
        ax.locator_params(nbins=10, axis='y')
        # plt.ticklabel_format(useOffset=False, style='plain')
        # ax.get_xaxis().get_major_formatter().set_scientific(False)
        # ax.get_yaxis().get_major_formatter().set_scientific(False)
        # Set y-axis limits and label
        plt.ylabel( '20-inch Soil Temperature (F)' )
        # plt.ylim(bottom=int(min(y)),top=int(max(y)))
        # Set grid
        plt.grid()
        # Set plot title
        plt.suptitle(name)
        # Save figure as png
        plt.savefig(outpath, bbox_inches='tight')
        plt.close(fig)
        return True
    except:
        return False
    

def GraphSoilTemp36(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['redish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['redish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # plt.ticklabel_format(useOffset=False, style='plain')
    # ax.get_xaxis().get_major_formatter().set_scientific(False)
    # ax.get_yaxis().get_major_formatter().set_scientific(False)
    # Set y-axis limits and label
    plt.ylabel( '36-inch Soil Temperature (F)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(bottom=int(min(y)),top=int(max(y)))
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilVWC4(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['ltbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '4-inch Soil Volumetric Water Content(%)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilVWC8(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['ltbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '8-inch Soil Volumetric Water Content(%)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilVWC20(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['ltbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '20-inch Soil Volumetric Water Content(%)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilVWC36(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['ltbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '36-inch Soil Volumetric Water Content(%)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilEC4(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['dkbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '4-inch Soil Saturation Extract Conductivity (mS/cm)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilEC8(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['dkbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '8-inch Soil Saturation Extract Conductivity (mS/cm)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilEC20(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['dkbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '20-inch Soil Saturation Extract Conductivity (mS/cm)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

def GraphSoilEC36(name,outpath,xlist,ylist):
    # Output path: sitename\sitename-element.png
    # Configure graph figure
    x = xlist
    y = ylist
    fig = graph_getfigure()
    ax = fig.add_subplot(111)
    # Plot data
    plt.scatter( x, y, color=colors['dkbluish'], marker='o', s=2)
    # plt.plot( x, y, color=colors['ltbluish'], linewidth=2.0)
    # Set x-axis data labels
    plt.xlabel( 'Date' )
    locs = plt.xticks()[0]
    labels = [item.get_text() for item in ax.get_xticklabels()]
    loclen = len(locs)
    for k in range(0,loclen):
        labels[k] = UTCms_to_localstring(int(locs[k]))
    ax.set_xticklabels(labels, rotation=45)
    # ax.yaxis.get_major_formatter().set_scientific(False)
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    # Set y-axis limits and label
    plt.ylabel( '36-inch Soil Saturation Extract Conductivity (mS/cm)' )
    ax.locator_params(nbins=10, axis='y')
    # plt.ylim(0,110)
    # Set grid
    plt.grid()
    # Set plot title
    plt.suptitle(name)
    # Save figure as png
    plt.savefig(outpath, bbox_inches='tight')
    plt.close(fig)
    return True

