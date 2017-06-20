# This should be place in ~ (home dir).
# This is used to specifiy caffe mode and data file name information

from kzpy3.utils import *

MLK_pm_lat,MLK_pm_lon = 37.881556,-122.278434
MLK_pm2_lat,MLK_pm2_lon = 37.881496, -122.278552 # 12 meters from pitcher's mound.

RFS_lat,RFS_lon = 37.91590,-122.3337223
RFS_lat2,RFS_lon2 = 37.915846, -122.333404 # 28 meters from field center.

M_1408_lat,M_1408_lon = 37.881401062, -122.27230072 #37.8814082,-122.2722957

miles_per_deg_lat = 68.94
miles_per_deg_lon_at_37p88 = 54.41
meters_per_mile = 1609.34

GPS2_lat_orig = M_1408_lat
GPS2_long_orig = M_1408_lon
GPS2_radius_meters = 800000000


RFS_start_lat,RFS_start_lon = 37.916731,-122.334096
RFS_end_lat,RFS_end_lon = 337.918258,-122.3342703

GPS2_radius_meters = 938442714

def lat_lon_to_dist_meters(lat_A,lon_A,lat_B,lon_B):
        dx = (lat_A-lat_B)*miles_per_deg_lat*meters_per_mile
        dy = (lon_A-lon_B)*miles_per_deg_lon_at_37p88*meters_per_mile
        return np.sqrt(dx**2+dy**2)