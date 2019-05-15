from math import sin, cos, atan2, sqrt, degrees, radians, pi
from geopy.distance import great_circle as distance
from geopy.point import Point

# https://stackoverflow.com/questions/27461634/calculate-distance-between-a-point-and-a-line-segment-in-latitude-and-longitude

def midpoint(a, b):
    a_lat, a_lon = radians(a.latitude), radians(a.longitude)
    b_lat, b_lon = radians(b.latitude), radians(b.longitude)
    delta_lon = b_lon - a_lon
    B_x = cos(b_lat) * cos(delta_lon)
    B_y = cos(b_lat) * sin(delta_lon)
    mid_lat = atan2(
        sin(a_lat) + sin(b_lat),
        sqrt(((cos(a_lat) + B_x)**2 + B_y**2))
    )
    mid_lon = a_lon + atan2(B_y, cos(a_lat) + B_x)
    mid_lon = (mid_lon + 3*pi) % (2*pi) - pi
    return Point(latitude=degrees(mid_lat), longitude=degrees(mid_lon))


def calGeoDistance(point, point_line_1, point_line_2):
    d = distance(midpoint(point_line_1, point_line_2), point)
    return d.km
'''
a = Point(latitude=59.9050401935882, longitude=10.7196405787775)
b = Point(latitude=59.9018650448204, longitude=10.7109989561813)
p = Point(latitude=59.429105, longitude=10.6542116666667)

d = distance(midpoint(a, b), p)
print(d.meters)
'''