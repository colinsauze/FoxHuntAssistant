# FoxHuntAssistant
An application to assist with amateur radio inverse "fox hunts". 
This is where you find a remote station by calling them on radio and having them tell you a bearing using direction finding equipment. 

This program takes your current location from GPSD and asks for the bearing to the remote station. It then uses KML to generate a 
triangular shape starting from your current location and heading in the direction of the remote station. Where these triangles overlap 
should reveal the location of the hidden station. The resulting KML files can be viewed in Google Earth or Marble. 

This software has only been tested on Ubuntu Linux 14.04 and 16.04, but should at least work on other Linux distributions.

To run it just execute get_cone.sh, this calls generate_cone.py with the current latitude and longitude from GPSD. It will ask you for the
angle of the latest run. It will then create a new KML file called coneXXX.kml where XXX is an incrementing number. 

![example]

[example]: https://github.com/colinsauze/FoxHuntAssistant/raw/master/foxhunt.png "Example output"
