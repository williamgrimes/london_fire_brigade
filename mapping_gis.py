import pandas as pd

import folium
from folium import plugins
from bng_to_latlon import OSGB36toWGS84


class Mapping(object):
    """methods for mapping incidents"""

    LONDON_COORDINATES = (51.51808736193663, -0.2102070877154833)  # centre map

    def get_lat_long_coords(data_frame):
        """returns a long and lat from easting and northing"""
        coords_list = []
        for index, row in data_frame.iterrows():
            coords_list.append(
                list(OSGB36toWGS84(row.easting/10, row.northing/10))
            )
            coords = pd.DataFrame(coords_list, columns=['long', 'lat'])
        return coords

    def plot_heatmap(coords):
        """returns a heatmap from coordinates data"""
        basemap = folium.Map(location=LONDON_COORDINATES,
                             tiles='stamentoner', zoom_start=10)
        heatmap = plugins.HeatMap(
            zip(coords['long'], coords['lat']),
            gradient={0.4: 'yellow', 0.65: 'orange', 1: 'red'},
            min_opacity=0.3,
            radius=10
        )
        heatmap = basemap.add_children(heatmap)
        return heatmap

    def overlay_point_map(basemap, data_frame):
        """plots point map over existing basemap"""
        for index, row in data_frame.iterrows():
            folium.CircleMarker(
                location=list(OSGB36toWGS84(row.easting/10, row.northing/10)),
                radius=25,
                popup=('Incident #: ' + str(row.IncidentNumber)),
                color='#3186cc',
                fill_color='#3186cc'
                ).add_to(basemap)
        return basemap

    def plot_point_map(data_frame):
        """plots point map"""
        basemap = folium.Map(location=LONDON_COORDINATES,
                             tiles='stamentoner', zoom_start=10)
        point_map = Mapping.overlay_point_map(basemap, data_frame)
        return point_map
