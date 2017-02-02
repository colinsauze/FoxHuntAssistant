#!/usr/bin/python

#script to generate a triangle in KML that fans out from the a lat/lon specified as command line arguments and at an angle entered into a prompt

#MIT License

#Copyright (c) 2017 Colin Sauze

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import math, glob, sys, os

#returns the coordinates of a point a given distance and bearing from an origin point
def project_point(bearing,dist,lat1,lon1):
    #d = angular distance covered on earth's surface
    dist = dist/6367  

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    bearing = math.radians(bearing)

    lat2 = math.asin( math.sin(lat1)*math.cos(dist) + math.cos(lat1)*math.sin(dist)*math.cos(bearing) )
    lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(dist)*math.cos(lat1), math.cos(dist)-math.sin(lat1)*math.sin(lat2))

    if (math.isnan(lat2) or math.isnan(lon2)):
        return None
        
    #print "projecting %f,%f by %f on a heading of %f = %f,%f" % (math.degrees(lat1),math.degrees(lon1),dist*6367,math.degrees(bearing),math.degrees(lat2),math.degrees(lon2))
    destpos = math.degrees(lat2),math.degrees(lon2)
    return destpos



#get the angle
try:
    print "Enter angle"
    angle=int(raw_input())
except ValueError:
    print "Not a number"

angle_min = angle-15
if angle_min<0:
    angle_min = angle_min + 360

angle_max = angle+15
if angle_max>359:
    angle_max = angle_max - 360

#make 3 points to form a triangle, our current location, and points 10km away at the angle +/- 15 degrees

lat=float(sys.argv[1])
lon=float(sys.argv[2])

point1=project_point(angle_min,10.0,lat,lon)
point2=project_point(angle_max,10.0,lat,lon)

filelist = glob.glob("cone*.kml")
maxnum=0


#calculate the filename 
for filename in filelist:
    filenum=filename.replace("cone","")
    filenum=filenum.replace(".kml","")

    try:
	if int(filenum) > maxnum:
	    maxnum = int(filenum)
    except ValueError:
	print "non-integer name %s" % (filename)
        
filename=("cone%03d.kml") % (maxnum+1)
print filename

outfile = open(filename,"w")

#write some KML

outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \
<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\" xmlns:atom=\"http://www.w3.org/2005/Atom\"> \
<Document>")


outfile.write( "    <Placemark><name>Untitled Polygon</name> \
	<Polygon> <tessellate>1</tessellate> <outerBoundaryIs><LinearRing> <coordinates> \
			%f,%f,0 %f,%f,0 %f,%f,0 %f,%f,0  \
		    </coordinates> </LinearRing> </outerBoundaryIs> </Polygon> </Placemark>" % (lon,lat,point1[1],point1[0],point2[1],point2[0],lon,lat))

outfile.write("</Document></kml>")

outfile.close()



