import folium
from folium import Choropleth, Circle, Marker, Icon, Map, TileLayer
from folium.plugins import HeatMap, MarkerCluster
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.express as px

location=[41.387214, 2.148976]

# We create the Choropleth map with the districts

def create_choro(_map, geo_, df_, columns_):
    _map = folium.Map(location, zoom_start=13)
    folium.Choropleth(
    geo_data=geo_,
    data=df_,
    columns=columns_,
    key_on='properties.NOM', 
    fill_color='PRGn', 
    fill_opacity=0.7, 
    line_opacity=0.5,
    ).add_to(_map)
    return _map

# This function is used for getting all the different values of a given geojson

def get_variables(geo, _list):
    for i in geo["features"]:
        name = i["properties"]['NOM_PARADA']
        # address =  i["properties"]['ADRECA']
        lat = i['geometry']['coordinates'][1]
        lon = i['geometry']['coordinates'][0]   
        type_ = {"typepoint":   
                            {"type": "Point", 
                            "coordinates": [lat, lon]}}
        _list.append({"name":name, "lat":lat, "lon":lon, "type":type_})
    return _list

def get_bicing(data, new_list):
    for i in data:
        name = i["name"]
        station_id = i['station_id']
        lat = i["lat"]
        lon = i["lon"]
        capacity = i["capacity"]
        new_list.append({"name":name, "station_id": station_id, "latitude":lat, "longitude":lon, "capacity": capacity}) 
        bicing = pd.DataFrame(new_list)
    return bicing

# We create animated maps in order to plot the year variables

def plot_map(geo_json, df_, match_location, value_plotted, animation, palette):
    fig = px.choropleth_mapbox(data_frame=df_,
        geojson=geo_json,
        locations=df_[match_location],
        featureidkey = 'properties.NOM',
        color=value_plotted,
        center={'lat':41.38879,  'lon':2.15899},
        mapbox_style='open-street-map',
        zoom=10,
        color_continuous_scale=palette,
        animation_frame=animation,
        labels={'districtes' : 'Nom_Districte_baixa'},
        width=850,  
        height=650)
    return fig


# With this function we create the feature group 

def get_feature(name, base):
    return folium.FeatureGroup(name = name, show=False).add_to(base)

# We create a function for ploting the Heatmap

def heat_map(df_, feature, radius, color1, color2, color3, level1, level2, level3  ):
    return HeatMap(data=df_[["latitude", "longitude"]], radius=radius, gradient = {level1: color1, level2: color2, level3: color3}).add_to(feature)
    
    