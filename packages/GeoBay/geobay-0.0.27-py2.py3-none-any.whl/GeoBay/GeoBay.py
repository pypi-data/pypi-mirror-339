"""Main module."""
#ipyleaflet module
from ipyleaflet import Map as IpyleafletMap, TileLayer, GeoJSON, LayersControl, ImageOverlay, VideoOverlay, WMSLayer
import geopandas as gpd
from ipywidgets import Color

class CustomIpyleafletMap(IpyleafletMap):
    def __init__(self, center, zoom=12, **kwargs):
        # Initialize the map with the center and zoom parameters
        super().__init__(center=center, zoom=zoom, **kwargs)
        
    def add_basemap(self, basemap_name: str):
        """
        Adds a basemap to the map.

        Parameters:
        - basemap_name (str): The name of the basemap, e.g., "OpenStreetMap", 
          "Esri.WorldImagery", "OpenTopoMap".
        
        Returns:
        - None
        """
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
        """
        Adds a layer control widget to manage layers on the map.

        Returns:
        - None
        """
        control = LayersControl()
        self.add_control(control)

    def add_vector(self, vector_data):
        """
        Adds vector data to the map. Supports formats that can be read by GeoPandas 
        (GeoJSON, Shapefile, etc.).

        Parameters:
        - vector_data (str or GeoDataFrame): File path to a vector dataset 
          (Shapefile, GeoJSON) or a GeoPandas GeoDataFrame.

        Returns:
        - None
        """
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
        """
        Adds a Cloud Optimized GeoTIFF (COG) as a raster layer.

        Parameters:
        - url (str): URL or path to the COG.
        - name (str): Optional name for the layer.
        - colormap (dict or str): Optional colormap.
        - opacity (float): Opacity of the layer.
        """
        tile_layer = TileLayer(
            url=url,
            name=name or "Raster Layer",
            opacity=opacity
        )
        self.add_layer(tile_layer)

    def add_image(self, url, bounds, opacity=1.0):
        """
        Adds a static image or GIF overlay to the map.

        Parameters:
        - url (str): URL to the image or GIF.
        - bounds (tuple): ((south, west), (north, east)) coordinate bounds.
        - opacity (float): Opacity of the image overlay.
        """
        image_layer = ImageOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(image_layer)

    def add_video(self, url, bounds, opacity=1.0):
        """
        Adds a video overlay to the map.

        Parameters:
        - url (str or list): URL(s) to the video file(s).
        - bounds (tuple): ((south, west), (north, east)) coordinate bounds.
        - opacity (float): Opacity of the video overlay.
        """
        video_layer = VideoOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(video_layer)

    def add_wms_layer(self, url, layers, name=None, format='image/png', transparent=True, **extra_params):
        """
        Adds a WMS (Web Map Service) layer to the map.

        Parameters:
        - url (str): Base WMS endpoint.
        - layers (str): Comma-separated layer names.
        - name (str): Optional display name.
        - format (str): Image format, default is 'image/png'.
        - transparent (bool): Whether the layer is transparent.
        - extra_params: Additional WMS parameters.
        """
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
        """
        Displays the ipyleaflet map.
        """
        return self
    

