# Main module.

from ipyleaflet import Map as IpyleafletMap, TileLayer, GeoJSON, LayersControl, ImageOverlay, VideoOverlay, WMSLayer
import geopandas as gpd

class CustomIpyleafletMap(IpyleafletMap):
    """
    A custom wrapper around ipyleaflet.Map with additional helper methods
    for adding basemaps, vector data, raster layers, images, videos, and WMS layers.
    """

    def __init__(self, center, zoom=12, **kwargs):
        """
        Initialize the custom map.

        Args:
            center (tuple): Latitude and longitude of the map center.
            zoom (int, optional): Zoom level of the map. Defaults to 12.
            **kwargs: Additional keyword arguments for ipyleaflet.Map.
        """
        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_basemap(self, basemap_name: str):
        """
        Add a basemap layer to the map.

        Args:
            basemap_name (str): Name of the basemap ('OpenStreetMap', 'Esri.WorldImagery', or 'OpenTopoMap').

        Raises:
            ValueError: If the basemap name is not supported.
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
        Add a control to toggle map layers on and off.
        """
        control = LayersControl()
        self.add_control(control)

    def add_vector(self, vector_data):
        """
        Add a vector layer to the map from a file path or GeoDataFrame.

        Args:
            vector_data (str or geopandas.GeoDataFrame): Path to a vector file or a GeoDataFrame.

        Raises:
            ValueError: If the input is not a valid file path or GeoDataFrame.
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
        Add a raster tile layer to the map.

        Args:
            url (str): URL template for the raster tiles.
            name (str, optional): Layer name. Defaults to "Raster Layer".
            colormap (optional): Colormap to apply (not used here but reserved).
            opacity (float, optional): Opacity of the layer (0.0 to 1.0). Defaults to 1.0.
        """
        tile_layer = TileLayer(
            url=url,
            name=name or "Raster Layer",
            opacity=opacity
        )
        self.add_layer(tile_layer)

    def add_image(self, url, bounds, opacity=1.0):
        """
        Add an image overlay to the map.

        Args:
            url (str): URL of the image.
            bounds (list): Bounding box of the image [[south, west], [north, east]].
            opacity (float, optional): Opacity of the image. Defaults to 1.0.
        """
        image_layer = ImageOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(image_layer)

    def add_video(self, url, bounds, opacity=1.0):
        """
        Add a video overlay to the map.

        Args:
            url (str): URL of the video.
            bounds (list): Bounding box for the video [[south, west], [north, east]].
            opacity (float, optional): Opacity of the video. Defaults to 1.0.
        """
        video_layer = VideoOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(video_layer)

    def add_wms_layer(self, url, layers, name=None, format='image/png', transparent=True, **extra_params):
        """
        Add a WMS (Web Map Service) layer to the map.

        Args:
            url (str): WMS base URL.
            layers (str): Comma-separated list of layer names.
            name (str, optional): Display name for the layer. Defaults to "WMS Layer".
            format (str, optional): Image format. Defaults to 'image/png'.
            transparent (bool, optional): Whether the background is transparent. Defaults to True.
            **extra_params: Additional parameters to pass to the WMSLayer.
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
        Display the map in a Jupyter notebook or compatible environment.

        Returns:
            ipyleaflet.Map: The configured map.
        """
        return self
