
from math import *


tile_size = 256


class MapTile:
    zoom = 0
    x = 0
    y = 0

    def __init__(self, zoom, x, y):
        self.zoom = zoom
        self.x = x
        self.y = y

    # convert map tile to bounding box (EPSG:4326 WGS-84 format)
    def xyz_to_bbox_wgs84(self):
        bounding_box = dict()
        top = lat_to_bbox(self.y, self.zoom)
        left = lon_to_bbox(self.x, self.zoom)
        bottom = lat_to_bbox(self.y + 1, self.zoom)
        right = lon_to_bbox(self.x + 1, self.zoom)

        bounding_box['top_left'] = "{}, {}".format(top, left)
        bounding_box['bottom_right'] = "{}, {}".format(bottom, right)
        return bounding_box


# convert Lat value to BBox.
def lat_to_bbox(y, z):
    n = pi - 2.0 * pi * y / pow(2, float(z))
    return 180.0 / pi * atan(0.5 * (exp(n) - exp(-n)))


# convert Lon value to BBox.
def lon_to_bbox(x, z):
    return float(x) / pow(2.0, float(z)) * 360.0 - 180.0


# find marker position on tile from longitude, latitude
def marker_position_of_lon_lat(lon, lat, zoom):

    # Length and width are converted to radians
    # λ = lmb , φ = fi
    lmb = lon * pi / 180
    fi = lat * pi / 180
    # print('λ =', lmb, 'φ=', fi)

    # Length and width are transformed by the
    # log (tan φ + 1 / cos φ)
    # lmb is unchanged
    cos_fi = 1 / cos(fi)
    new_fi = log(tan(fi) + cos_fi)
    # print('new fi', new_fi)

    # Length and width are transformed into the map coordinate system.
    # This starts at the top left with [0,0] and ends at the bottom right
    # with [1,1]:
    x_pos = (1 + lmb / pi) / 2
    y_pos = (1 - new_fi / pi) / 2
    # print('X Position', x_pos, 'Y Position', y_pos)

    #  Calculate tile number
    # ======================
    # tile_x = floor(x_pos * pow(2, zoom))
    # tile_y = floor(y_pos * pow(2, zoom))
    # print('Calculate tile number zoom/tx/ty', zoom, tile_x, tile_y)
    # as well as the tile size in pixels tile_size = 256 we compute

    # the position of the marker:
    frac_x, whole_x = modf(x_pos * pow(2, zoom))
    frac_y, whole_y = modf(y_pos * pow(2, zoom))
    # print('frac_x, frac_y', frac_x, frac_y)
    # marker_x = floor(fractions.())

    position_x = floor(frac_x * tile_size)
    position_y = floor(frac_y * tile_size)
    # print('px, py', position_x, position_y)
    return position_x, position_y
