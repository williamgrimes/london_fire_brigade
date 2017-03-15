"""functions for plotting GIS maps of incidents including mapping class"""

import pandas as pd

import folium
from folium import plugins
from bng_to_latlon import OSGB36toWGS84


def get_lat_long_coords(data_frame):
    """returns a long and lat from easting and northing"""
    coords_list = []
    for index, row in data_frame.iterrows():
        coords_list.append(
            list(OSGB36toWGS84(row.easting/10, row.northing/10))
        )
        coords = pd.DataFrame(coords_list, columns=['long', 'lat'])
    return coords


class Mapping():
    """methods for mapping incidents"""

    def __init__(self):
        self.london_coordinates = (51.51, -0.21)  # centre map
        self.tiles = 'stamentoner'
        self.zoom = 10
        self.hm_gradient={0.3: 'yellow', 0.55: 'orange', 1: 'red'}
        self.hm_min_opacity=0.7
        self.hm_radius=10
        self.dict_size = {'None': 20, 0: 20,
                          'Small': 40, 1: 40,
                          'Medium': 60, 2: 60,
                          'Large': 80, 3: 80,
                          '5+': 100, 4: 100}

    def plot_heatmap(self, data_frame):
        """returns a heatmap from coordinates data"""
        coords = get_lat_long_coords(data_frame)
        basemap = folium.Map(location=self.london_coordinates,
                             tiles=self.tiles, zoom_start=self.zoom)
        heatmap = plugins.HeatMap(
            zip(coords['long'], coords['lat']),
            gradient=self.hm_gradient,
            min_opacity=self.hm_min_opacity,
            radius=self.hm_radius
        )
        heatmap = basemap.add_children(heatmap)
        return heatmap

    def overlay_point_map(self, data_frame, basemap):
        """plots point map over existing basemap"""
        data_frame = data_frame.fillna('None')
        for index, row in data_frame.iterrows():
            size = self.dict_size[row.ActionBased]
            html="<small> \
                <h3> Incident #: " + str(row.IncidentNumber) +  "</h3> \
                <p> \
                <b>Action Based: </b>" + str(row.ActionBased) + "<br> \
                <b>Action Parent: </b>" + str(row.ActionParent) + "<br> \
                <b>Action: </b>" + str(row.Action) + "<br> \
                <b>Motive: </b>" + str(row.Motive) + "<br> \
                <b>BriefDescriptionOfFire: </b><i>" + \
                str(row.BriefDescriptionOfFire) +"</i><br> \
                <b>FurtherInformation: </b><i>" + \
                str(row.FurtherInformation) + "</i><br> \
                <b>PropertyType: </b><i>" + \
                str(row.PropertyType) +"</i><br> \
                <b>Date and time of call: </b>" + str(row.DDDateTimeOfCall) + "<br> \
                </p> \
                </small>"
            iframe = folium.element.IFrame(html=html, width=450, height=200)
            popup = folium.Popup(iframe, max_width=500)
            folium.CircleMarker(
                location=list(OSGB36toWGS84(row.easting/10, row.northing/10)),
                radius=size,
                popup=popup,
                color='#00ffffff', #none
                fill_color='#ff3300'#red
                ).add_to(basemap)
        return basemap

    def plot_point_map(self, data_frame):
        """plots point map"""
        coordinates = self.london_coordinates
        basemap = folium.Map(location=coordinates, tiles=self.tiles,
                             zoom_start=self.zoom)
        point_map = Mapping.overlay_point_map(self, data_frame, basemap)
        return point_map
