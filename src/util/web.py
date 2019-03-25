import textwrap

import arcpy


country={"":"",
         "ID":"USA",
         "NE":"USA",
         "MT":"USA",
         "ND":"USA",
         "NV":"USA",
         "SD":"USA",
         "OR":"USA",
         "UT":"USA",
         "WA":"USA",
         "WY":"USA",
         "AB":"CAN",
         "BC":"CAN",
         "MB":"CAN",
         "SK":"CAN"}

class Station:
    def __init__(self,station,inventory,webinv,domaintable):
        self.station = station
        self.edited = "2013-07-31"
        self.xmin = "-12498505.720801364"
        self.ymin = "5808115.744858614"
        self.xmax = "-12458185.18838099"
        self.ymax = "5826116.66501975"
        self.name = "Glendive"
        self.state = "MT"
        self.latitude = "47.1065"
        self.longitude = "-104.7183"
        self.elevft = "5,280"
        self.elevm = "398.0"
        self.network = "U.S. Cooperative Network identification number"
        self.getvalues(station,inventory,webinv,domaintable)
        
    def getvalues(self,station,invtable,webinv,domaintable):
        searchstr = '"Station" = ' + "'" + station + "'"
        tblRows = arcpy.SearchCursor(invtable,searchstr)
        for row in tblRows:
            self.station = str(row.getValue("Station"))
            self.edited = str(row.getValue("ET_EDITED").strftime("%Y-%m-%d"))
            self.name = str(row.getValue("Name"))
            self.state = str(row.getValue("State"))
            self.latitude = str(row.getValue("Latitude"))
            self.longitude = str(row.getValue("Longitude"))
            self.elevft = "{:,}".format((int(row.getValue("Elevation")*3.2808)))
            self.elevm = str(row.getValue("Elevation"))
            self.network = str(row.getValue("Network")) + ":" + self.getdomaindescription(row.getValue("Network"),domaintable)
        # Get bounding coordinates for web map
        searchstr = '"Station" = ' + "'" + station + "'"
        tblRows = arcpy.SearchCursor(webinv,searchstr)
        for row in tblRows:
            point = row.getValue("Shape")
            part = point.getPart()
            self.xmin = str(part.X - 40320)
            self.ymin = str(part.Y - 18000)
            self.xmax = str(part.X + 40320)
            self.ymax = str(part.Y + 18000)
            # self.xmin = "-12498505.720801364"
            # self.ymin = "5808115.744858614"
            # self.xmax = "-12458185.18838099"
            # self.ymax = "5826116.66501975"
  
    def getdomaindescription(self,elementval,domaintable):
        domaindesc = ""
        searchstr = '"Code" = ' + "'" + elementval + "'"
        tblRows = arcpy.SearchCursor(domaintable,searchstr)
        for row in tblRows:
            domaindesc = str(row.getValue("Description"))
        return domaindesc

class StationElements2:
    def __init__(self, station, stattbl, domaintable):
        self.elements = self.getelements(station,stattbl,domaintable)

    def getelements(self,station,stattbl,domaintable):
        elements = []
        searchstr = '"FIRST_Station" = ' + "'" + station + "'"
        tblRows = arcpy.SearchCursor(stattbl,searchstr)
        for row in tblRows:
            elementval = row.getValue("Element") + ":" + self.getdomaindescription(row.getValue("Element"),domaintable)
            startval = row.getValue("FIRST_Date")
            endval = row.getValue("LAST_Date")
            ndays = (endval-startval).days
            nyrs = str(endval.year - startval.year)
            obsvalue = row.getValue("FREQUENCY")
            startval = str(startval.year) + "-" + str(startval.month) + "-" + str(startval.day)
            #startval = startval.strftime("%Y-%m-%d")
            endval = str(endval.year) + "-" + str(endval.month) + "-" + str(endval.day)
            #endval = endval.strftime("%Y-%m-%d")
            if obsvalue is not None:
                obsval = "{:,}".format(obsvalue)
            else:
                obsval = "0"
            if ndays > 0:
                percentage = str(int((float(obsvalue)/float(ndays))*100.0))
                percentval = str(percentage)+"%"
            else:
                percentval = "0%"
            elements.append([elementval,startval,endval,nyrs,obsval,percentval])
        return elements
    
    def getdomaindescription(self,elementval,domaintable):
        domaindesc = ""
        searchstr = '"Code" = ' + "'" + elementval + "'"
        tblRows = arcpy.SearchCursor(domaintable,searchstr)
        for row in tblRows:
            domaindesc = str(row.getValue("Description"))
        return domaindesc

class StationElements:
    def __init__(self, station, invtable, domaintable):
        self.elements = self.getelements(station,invtable.table,domaintable)

    def getelements(self,station,invtable,domaintable):
        elements = []
        searchstr = '"Station" = ' + "'" + station + "'"
        tblRows = arcpy.SearchCursor(invtable,searchstr)
        for row in tblRows:
            elementval = row.getValue("Element") + ":" + self.getdomaindescription(row.getValue("Element"),domaintable)
            startval = str(row.getValue("StartYear"))
            endval = str(row.getValue("EndYear"))
            recordval = str(row.getValue("RecordLength"))
            obsvalue = row.getValue("Observations")
            if obsvalue is not None:
                obsval = "{:,}".format(obsvalue)
            else:
                obsval = "0"
            perval = row.getValue("Percentage")
            if perval is not None:
                percentval = str(row.getValue("Percentage"))+"%"
            else:
                percentval = "0%"
            elements.append([elementval,startval,endval,recordval,obsval,percentval])
        return elements
    
    def getdomaindescription(self,elementval,domaintable):
        domaindesc = ""
        searchstr = '"Code" = ' + "'" + elementval + "'"
        tblRows = arcpy.SearchCursor(domaintable,searchstr)
        for row in tblRows:
            domaindesc = str(row.getValue("Description"))
        return domaindesc

class StationPage:
    def __init__(self, station, elements, fname):
        self.f = open(fname,"w")
        self.generate_block01()
        self.generate_block02(station)
        self.generate_block03()
        self.generate_block04(station)
        self.generate_block05()
        self.generate_block06(station)
        self.generate_block07(station)
        self.generate_block08()
        self.generate_block09(elements)
        self.generate_block10()
        self.generate_block11(station)
        self.generate_block12()

    def generate_block01(self):
        self.f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')

    def generate_block02(self,station):
        self.f.write ('<title>' + station.station + '</title>\n')

    def generate_block03(self):
        self.f.write(textwrap.dedent('''
        </head>
        <style>
        body{
            color: #000000;
            font-family: 'Open Sans',Helvetica,Arial,sans-serif;
            line-height: 1.2em;
            text-rendering: optimizelegibility;
        }
        h1{
        padding:5px 0 5px 0;
        margin:0px;
        font-size:1.7em;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        color:#000000;
        }
        h2{
        padding:5px 0 5px 0;
        margin:0px;
        font-size:1.5em;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        color:#000000;
        }
        h3{
        padding:5px 0 5px 0;
        margin:0px;
        font-size:1.3em;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        color:#791717;
        }
        h4{
        padding:5px 0 5px 0;
        margin:0px;
        font-size:1.1em;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        color:#000000;
        }
        h5{
        padding:5px 0 5px 0;
        margin:0px;
        font-size:0.9em;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        color:#000000;
        }
        h6{
        padding:5px 0 5px 0;
        margin:0px;
        font-size:0.7em;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        color:#000000;
        }
        p{
        text-align:justify;
        line-height:18px;
        letter-spacing: 1px;
        word-spacing: 1px;
        font-size: 1.0em;
        color:#000000;
        }
        a:link {
        color: #136799;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        text-decoration:none 
        }
        a:visited {
        color: #136799;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        }
        a:hover {
        color: #791717;
        text-decoration:underline;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        }
        a:active {
        color: #967D3A;
        font-family:'Bitter',Cambria,Georgia,Palatino,serif;
        }
        #footer a {
        text-decoration: none;
        color: #fff;
        }
        #footer a:hover {
        text-decoration: underline;
        }
        #footer {
        font-size: 8pt;
        overflow: hidden;
        clear: both;
        color: #fff;
        margin: 0 auto;
        margin-bottom: 5px;
        }
        #stations {
        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
        border-collapse:collapse;
        }
        #stations td, #stations th {
        font-size:0.85em;
        border:1px solid #98bf21;
        padding:3px 7px 2px 7px;
        }
        #stations th {
        font-size:0.85em;
        text-align:left;
        padding-top:5px;
        padding-bottom:4px;
        background-color:#A7C942;
        color:#ffffff;
        }
        #stations tr.alt td {
        color:#000000;
        background-color:#EAF2D3;
        }
        </style>
        <body>
        <h3><a href="http://www.cfc.umt.edu/mco/" target="_blank">Montana Climate Office</a></h3>'''
        ))

    def generate_block04(self,station):
        self.f.write('<a href="ftp://mco.cfc.umt.edu/ghcnd/daily/csv/' + station.station + '_daily.csv">(download measurement data for this station in CSV format)</a>')

    def generate_block05(self):
        self.f.write(textwrap.dedent('''
        <br/><br/>
        <div>
        <table id="stations">
        <tbody>'''))

    def generate_block06(self,station):
        """
        part1 = '''<tr><td colspan="2"><b>Station Details</b>&nbsp;&nbsp;<small>(<a href='http://mco.maps.arcgis.com/apps/OnePane/basicviewer/index.html?&extent='''
        part2 = '{"xmin":' + station.xmin + ',"ymin": ' + station.ymin + ',"xmax": ' + station.xmax + ',"ymax": ' + station.ymax + ','
        part3 = '''"spatialReference":{"wkid":3857}}&appid=e594e6c1a2b845c5b141ca578ff3bc23' target="_blank">view location map in new window</a>)</small></td></tr>'''
        textstr = part1 + part2 + part3 + "\n"
        """
        locx = str((float(station.xmin)+float(station.xmax))/2)
        locy = str(((float(station.ymin)+float(station.ymax))/2)+150)
        part1 = '''<tr><td colspan="2"><b>Station Details</b>&nbsp;&nbsp;(<a href='http://mco.maps.arcgis.com/home/webmap/viewer.html?marker='''
        part2 = locx + ";" + locy + ";102100;GHCN Station;;" + station.name + "(" + station.station + ")"+ '''&level=11&webmap=4062a983ce4741338675c2a63dae85ee&mapOnly=true&extent='''
        part3 = station.xmin + '%2C' + station.ymin + '%2C' + station.xmax + '%2C' + station.ymax + "%2C102100'"
        part4 = ''' target="_blank">view location map in new window</a>)</td></tr>'''
        textstr = part1 + part2 + part3 + part4 + "\n"
        self.f.write(textstr)

    def generate_block07(self,station):
        if station.state <> "":
            part1 = ('<tr class="alt"><td>Station Name:</td><td>' + 
                     station.name + ', ' + station.state + 
                     '&nbsp;'  + country[station.state] + '</td></tr>')
        else:
            part1 = ('<tr class="alt"><td>Station Name:</td><td>' + 
                     station.name + '</td></tr>')       
        part2 = ('<tr><td>Station ID:</td><td>' + station.station + '</td></tr>')
        part3 = ('<tr class="alt"><td>Lat/Long:&sup2;</td><td>' + station.latitude + 
                 '&#176;,' + station.longitude + '&#176;</td></tr>')
        part4 = ('<tr><td>Elevation:</td><td>' + station.elevft + ' feet; ' + station.elevm + ' meters</td></tr>')
        part5 = ('<tr class="alt"><td>Network:</td><td>' + station.network + '</td>')
        textstr = part1 + part2 + part3 + part4 + part5
        self.f.write(textstr)

    def generate_block08(self):
        self.f.write(textwrap.dedent('''
        </tbody>
        </table>
        <br/>
        <table id="stations">
        <tbody>
        <tr><td><b>Element</b></td><td><b>Start</b></td><td><b>End</b></td><td><b>Years</b></td><td><b>Observations</b></td><td><b>Coverage&sup3;</b></td></tr>
        '''))

    def generate_block09(self,elements):
        index = 0
        for ele in elements.elements:
            if index % 2 == 0:
                self.f.write('<tr class="alt"><td>' + ele[0])
            else:
                self.f.write('<tr><td>' + ele[0])
            index = index + 1
            self.f.write('</td><td>' + ele[1] +
                         '</td><td>' + ele[2] + 
                         '</td><td>' + ele[3] + 
                         '</td><td>' + ele[4] + 
                         '</td><td>' + ele[5] + '</td></tr>')
    
        
    def generate_block10(self):
        self.f.write(textwrap.dedent('''
        </tbody>
        </table>
        <br/>
        '''))

    def generate_block11(self,station):
        self.f.write('<a href="http://www.ncdc.noaa.gov/' + 
                     'cdo-web/datasets/GHCND/stations/GHCND:'+ station.station + 
                     '/detail" target="_blank">Additional information</a> for this ' + 
                     'site is available at the National Oceanic and Atmospheric Administration (NOAA) ' +
                     'National Climatic Data Center (NCDC)')

    def generate_block12 (self):
        self.f.write(textwrap.dedent('''
        <hr>
        <div id="footer">
        <p>&sup1;  Dates are in standard ISO format (yyyy-mm-dd)</p>
        <p>&sup2; Coordinates are in the World Geodetic Coordinate System 1984</p>
        <p>&sup3; Coverage is an approximation of total completeness and the overall data range expressed as a percentage.</p>
        <p>Provided by the Montana Climate Office, Montana University System, College of Forestry and Conservation, University of Montana, 32 Campus Drive, Missoula, MT 59812-5076, Phone: 406-243-5521, Email: state.climatologist@umontana.edu</p>
        </div>
        </body>
        </html>
        '''))
        self.f.close()
#
# Code to test this class
#

if __name__ == "__main__":
    pass
    #  sta = Station("USC00454679","D:\MCO\Inventory.gdb")
    #  ele = StationElements("USC00454679","D:\MCO\InvTable.gdb")
    #  pg = StationPage(sta,ele,"D:\MCO\Test.html")
    