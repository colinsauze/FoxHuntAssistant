import math
import pandas

def get_angle_diff(angle1, angle2):
    diff = angle1 - angle2
    if diff < -180:
        diff = diff + 360
    elif diff > 180:
        diff = 0 - (360 - diff)
    return diff

def calculate_angle(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)    
    
    heading = math.degrees(math.atan2(math.sin(lon2-lon1)*math.cos(lat2), math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)))
    
    #make headings between 0 and 360 not -180 and +180
    if(heading<0):
        heading = heading + 360

    return heading

print("\"Date\",\"Time\",\"Lat\",\"Lon\",\"FoxLat\",\"FoxLon\",\"Calculated Angle\",\"Reported Angle\",\"Error\"")


for data_dir in ["data/2016", "data/2017", "data/2018", "data/2019", "data/2021"]:

    fox_location = open(data_dir + "/fox_location","r")

    fox_loc_str = fox_location.read()

    fox_lat = float(fox_loc_str.split(",")[0])
    fox_lon = float(fox_loc_str.split(",")[1])

    fox_location.close()

    data = pandas.read_csv(data_dir + "/logfile")

    for idx, row in data.iterrows():
        true_angle = calculate_angle(row['lat'], row['lon'], fox_lat, fox_lon)
        angle_diff = get_angle_diff(true_angle, row['angle'])
        print("%s,%s,%f,%f,%f,%f,%d,%d,%d" % (row['date'],row['time'],row['lat'],row['lon'],fox_lat,fox_lon,true_angle,row['angle'],angle_diff))


