import folium
import pandas as pd

data = pd.read_csv("Volcanoes.txt")
lat = list(data.LAT)
lon = list(data.LON)
elevation = list(data.ELEV)
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

Map = folium.Map(location = [40,-115], zoom_start = 6, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, el, name in zip(lat, lon, elevation, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(iframe), 
                               icon = folium.Icon(color = identify_colour(el), icon = 'circle')))
    
fgp = folium.FeatureGroup(name = "Population")
    
fgp.add_child(folium.GeoJson(data = (open("world.json", 'r', encoding='utf-8-sig')).read(), 
                           style_function = lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
                           else 'orange' if 10000000 < x['properties']['POP2005'] < 30000000 else 'red'}))

Map.add_child(fgv)
Map.add_child(fgp)
Map.add_child(folium.LayerControl())

Map.save("Volcanoes.html")