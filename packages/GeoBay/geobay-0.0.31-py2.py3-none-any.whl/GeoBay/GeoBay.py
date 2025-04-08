# Main module.

from ipyleaflet import Map as IpyleafletMap, TileLayer, GeoJSON, LayersControl, ImageOverlay, VideoOverlay, WMSLayer
import geopandas as gpd

class CustomIpyleafletMap(IpyleafletMap):
    def __init__(self, center, zoom=12, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_basemap(self, basemap_name: str):
        basemap_urls = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "Esri.WorldImagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
        }

        if basemap_name not in basemap_urls:
            raise ValueError(f"Basemap '{basemap_name}' is not supported.")

        basemap = TileLayer(url=basemap_urls[basemap_name])
        self.add_layer(basemap)

    def add_layer_control(self):
        control = LayersControl()
        self.add_control(control)

    def add_vector(self, vector_data):
        if isinstance(vector_data, str):
            gdf = gpd.read_file(vector_data)
        elif isinstance(vector_data, gpd.GeoDataFrame):
            gdf = vector_data
        else:
            raise ValueError("Input must be a file path or a GeoDataFrame.")

        geo_json_data = gdf.__geo_interface__
        geo_json_layer = GeoJSON(data=geo_json_data)
        self.add_layer(geo_json_layer)

    def add_raster(self, url, name=None, colormap=None, opacity=1.0):
        tile_layer = TileLayer(
            url=url,
            name=name or "Raster Layer",
            opacity=opacity
        )
        self.add_layer(tile_layer)

    def add_image(self, url, bounds, opacity=1.0):
        image_layer = ImageOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(image_layer)

    def add_video(self, url, bounds, opacity=1.0):
        video_layer = VideoOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(video_layer)

    def add_wms_layer(self, url, layers, name=None, format='image/png', transparent=True, **extra_params):
        wms_layer = WMSLayer(
            url=url,
            layers=layers,
            name=name or "WMS Layer",
            format=format,
            transparent=transparent,
            **extra_params
        )
        self.add_layer(wms_layer)

    def show_map(self):
        return self
