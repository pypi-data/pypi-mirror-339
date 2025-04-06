import folium
import pandas as pd
import math
import logging
import html
import branca
import matplotlib.pyplot as plt

import geopandas as gpd
from geopy.distance import geodesic
from folium import plugins
from folium.plugins import MarkerCluster

from .config import (
    MapConfig, EventConfig, FaultConfig, StationConfig,
    TILE_LAYER_CONFIGS
)
from .utils import (
    load_faults,
    load_stations_csv,
    calculate_distances_vectorized
)

logger = logging.getLogger(__name__)

class EventMap:
    """
    A revised approach that:
      - Merges event bounding box + site bounding box, then calls fit_bounds(...)
      - Uses min_zoom to effectively lock the user from zooming out too far
      - Adds or omits 'Repi' in event tooltips based on a new 'show_distance_in_tooltip' flag
      - If legend.csv missing, we show default fields (latitude, longitude, magnitude, ID).
      - If legend.csv present, we optionally override field labels, but can still skip Repi if desired.
    """

    def __init__(
        self,
        map_config: MapConfig,
        event_config: EventConfig,
        events_csv: str,
        legend_csv: str = None,
        x_col: str = None,
        y_col: str = None,
        location_crs: str = 'EPSG:4326',
        mandatory_mag_col: str = 'mag',
        calculate_distance: bool = True,
        fault_config: FaultConfig = None,
        station_config: StationConfig = None,
        show_distance_in_tooltip: bool = True,  # new flag
        log_level=logging.INFO
    ):
        logger.setLevel(log_level)
        self.map_config = map_config
        self.event_config = event_config
        self.fault_config = fault_config
        self.station_config = station_config

        self.events_csv = events_csv
        self.legend_csv = legend_csv
        self.x_col = x_col
        self.y_col = y_col
        self.location_crs = location_crs
        self.mandatory_mag_col = mandatory_mag_col
        self.calculate_distance = calculate_distance

        # new param controlling whether we show Repi in tooltips
        self.show_distance_in_tooltip = show_distance_in_tooltip

        # Data
        self.events_df = pd.DataFrame()
        self.legend_df = pd.DataFrame()
        self.stations_df = pd.DataFrame()
        self.faults_gdf = None

        # Folium objects
        self.map_object = None
        self.marker_group = None
        self.color_map = None

        # We'll store combined bounding lat/lon
        self.bounds = None

    def load_data(self):
        """Load events, optionally legend, optionally compute Repi, filter, color map, etc."""
        # 1) Load events
        try:
            self.events_df = pd.read_csv(self.events_csv)
            logger.info(f"Loaded {len(self.events_df)} events from '{self.events_csv}'.")
        except Exception as e:
            logger.error(f"Could not load events_csv='{self.events_csv}': {e}")
            return

        # 2) Legend
        self._load_legend()

        # 3) Convert X,Y -> lat,lon if needed
        self._convert_xy_to_latlon_if_needed()

        # 4) Validate mandatory magnitude col
        if self.mandatory_mag_col not in self.events_df.columns:
            logger.error(f"Mandatory magnitude column '{self.mandatory_mag_col}' missing.")
            return
        # ensure numeric
        self.events_df[self.mandatory_mag_col] = pd.to_numeric(
            self.events_df[self.mandatory_mag_col], errors='coerce'
        )
        self.events_df.dropna(subset=[self.mandatory_mag_col], inplace=True)

        # 5) Compute Repi if wanted
        if self.calculate_distance:
            logger.info("Calculating Repi distances (Haversine) from site.")
            self._compute_distances()  # populates events_df['Repi']

            # distance filter
            multiplier = self.event_config.event_radius_multiplier or 1.0
            dist_km = self.map_config.radius_km * multiplier
            before_cnt = len(self.events_df)
            self.events_df = self.events_df[self.events_df['Repi'] <= dist_km]
            logger.info(f"Distance filter removed {before_cnt - len(self.events_df)} events; "
                        f"{len(self.events_df)} remain within {dist_km} km of site.")

        # 6) Magnitude filter
        if self.event_config.vmin is not None:
            pre_count = len(self.events_df)
            self.events_df = self.events_df[
                self.events_df[self.mandatory_mag_col] >= self.event_config.vmin
            ]
            logger.info(f"vmin={self.event_config.vmin} removed {pre_count - len(self.events_df)} events.")
        if self.event_config.vmax is not None:
            pre_count = len(self.events_df)
            self.events_df = self.events_df[
                self.events_df[self.mandatory_mag_col] <= self.event_config.vmax
            ]
            logger.info(f"vmax={self.event_config.vmax} removed {pre_count - len(self.events_df)} events.")

        # 7) Color map
        self._build_colormap()

        # 8) Faults
        if self.fault_config and self.fault_config.include_faults:
            self._load_faults()

        # 9) Stations
        if self.station_config and self.station_config.station_file_path:
            self._load_stations()

        # 10) Compute combined bounding box from site radius + event coords
        self._compute_combined_bounds()

    def _load_legend(self):
        if not self.legend_csv:
            logger.info("No legend.csv provided. Will show default tooltips only.")
            return
        try:
            self.legend_df = pd.read_csv(self.legend_csv)
            logger.info(f"Loaded legend from '{self.legend_csv}'. Fields: {list(self.legend_df['Field'])}")
        except Exception as e:
            logger.warning(f"Could not load legend_csv='{self.legend_csv}': {e}. Using empty legend.")
            self.legend_df = pd.DataFrame()

    def _convert_xy_to_latlon_if_needed(self):
        has_latlon = ("latitude" in self.events_df.columns) and ("longitude" in self.events_df.columns)
        has_xy = (self.x_col is not None) and (self.y_col is not None)
        if not has_latlon and has_xy:
            logger.info(f"Converting {self.x_col},{self.y_col} from '{self.location_crs}' to EPSG:4326.")
            from pyproj import Transformer
            transformer = Transformer.from_crs(self.location_crs, 'EPSG:4326', always_xy=True)
            xs = self.events_df[self.x_col].values
            ys = self.events_df[self.y_col].values
            lon, lat = transformer.transform(xs, ys)
            self.events_df["longitude"] = lon
            self.events_df["latitude"] = lat

        self.events_df.dropna(subset=["latitude", "longitude"], inplace=True)

    def _compute_distances(self):
        # vectorized or geopy approach
        calculate_distances_vectorized(
            events_df=self.events_df,
            center_lat=self.map_config.latitude,
            center_lon=self.map_config.longitude,
            lat_col="latitude",
            lon_col="longitude",
            out_col="Repi"
        )

    def _build_colormap(self):
        if self.events_df.empty:
            logger.warning("No events left; skipping color map.")
            return
        vmin = self.event_config.vmin
        vmax = self.event_config.vmax
        mags = self.events_df[self.mandatory_mag_col]
        data_min, data_max = mags.min(), mags.max()

        if vmin is None:
            vmin = math.floor(data_min * 2) / 2.0
        if vmax is None:
            vmax = math.ceil(data_max * 2) / 2.0

        logger.info(f"Building color map from {vmin} to {vmax}, reversed={self.event_config.color_reversed}.")

        cmap = plt.get_cmap(self.event_config.color_palette)
        if self.event_config.color_reversed:
            cmap = cmap.reversed()

        color_list = [cmap(i / cmap.N) for i in range(cmap.N)]
        self.color_map = branca.colormap.LinearColormap(
            colors=color_list, vmin=vmin, vmax=vmax
        )
        self.color_map.caption = self.event_config.legend_title or "Magnitude"

    def _load_faults(self):
        logger.info(f"Loading faults from {self.fault_config.faults_gem_file_path}...")
        try:
            import geopandas as gpd
            gdf = load_faults(self.fault_config.faults_gem_file_path, self.fault_config.coordinate_system)
        except Exception as e:
            logger.error(f"Failed to load faults: {e}")
            return

        if not gdf.is_valid.all():
            logger.warning("Some fault geometries invalid; removing them.")
            gdf = gdf[gdf.is_valid]

        self.faults_gdf = gdf
        logger.info(f"Faults loaded. Found {len(gdf)} features.")

    def _load_stations(self):
        logger.info(f"Loading stations from {self.station_config.station_file_path}...")
        try:
            df = load_stations_csv(
                self.station_config.station_file_path,
                self.station_config.coordinate_system
            )
        except Exception as e:
            logger.error(f"Failed to load stations: {e}")
            return
        self.stations_df = df
        logger.info(f"Stations loaded. Found {len(self.stations_df)} stations.")

    def _compute_combined_bounds(self):
        """
        Merge bounding box from site radius_km + event coords,
        so we can fit_bounds(...) to that region.
        """
        lat_c = self.map_config.latitude
        lon_c = self.map_config.longitude
        # approximate bounding box around site
        multiplier = self.event_config.event_radius_multiplier or 1.0
        dist_km = self.map_config.radius_km * multiplier

        d_lat = dist_km / 111.0
        cos_lat = math.cos(math.radians(lat_c))
        if abs(cos_lat) < 1e-6:
            cos_lat = 1e-6
        d_lon = dist_km / (111.0 * cos_lat)

        box_min_lat = lat_c - d_lat
        box_max_lat = lat_c + d_lat
        box_min_lon = lon_c - d_lon
        box_max_lon = lon_c + d_lon

        # expand to include event coords
        all_lats = [box_min_lat, box_max_lat]
        all_lons = [box_min_lon, box_max_lon]

        if not self.events_df.empty:
            all_lats.extend(self.events_df["latitude"].values.tolist())
            all_lons.extend(self.events_df["longitude"].values.tolist())

        # optional: if you want stations included in bounding
        if not self.stations_df.empty:
            all_lats.extend(self.stations_df["latitude"].values.tolist())
            all_lons.extend(self.stations_df["longitude"].values.tolist())

        min_lat, max_lat = min(all_lats), max(all_lats)
        min_lon, max_lon = min(all_lons), max(all_lons)

        self.bounds = [[min_lat, min_lon], [max_lat, max_lon]]
        logger.info(
            f"Combined bounds: lat=({min_lat}, {max_lat}), lon=({min_lon}, {max_lon})."
        )

    def get_map(self):
        """
        Build the map, add layers, then fit_bounds(...) to self.bounds.
        The combination of self.map_config.min_zoom_level + this bounding
        box effectively restricts how far the user can zoom out.
        """
        self._initialize_map()

        # Feature group for events
        self.marker_group = folium.FeatureGroup(name="Events")

        # Add epicentral circles first if you want them behind the markers
        self._add_epicentral_distance_layer()

        # Then events
        self._add_event_markers()
        self._add_marker_cluster_layer()
        self._add_heatmap_layer()

        # Faults
        if self.faults_gdf is not None and not self.faults_gdf.empty:
            self._add_faults()

        # Stations
        if not self.stations_df.empty:
            self._add_stations()

        # site marker, tiles, etc.
        self._add_site_marker()
        self._add_tile_layers()
        self._add_layer_control()
        self._add_fullscreen_button()
        self._add_color_legend()

        # Now fit bounds
        self._fit_bounds()

        return self.map_object

    def _initialize_map(self):
        logger.info("Initializing map with base_zoom, min_zoom, max_zoom.")
        self.map_object = folium.Map(
            location=[self.map_config.latitude, self.map_config.longitude],
            zoom_start=self.map_config.base_zoom_level,
            min_zoom=self.map_config.min_zoom_level,  # e.g., 4 or 5
            max_zoom=self.map_config.max_zoom_level,
            control_scale=True
        )
    
    def _add_event_markers(self):
        """
        Build tooltips from either:
          - The legend_df if present
          - Otherwise default fields
        Conditionally show Repi if self.show_distance_in_tooltip=True AND we have Repi col.
        """
        legend_map = {}
        for _, row in self.legend_df.iterrows():
            f_ = str(row["Field"]).strip()
            lbl_ = str(row["Legend"]).strip()
            legend_map[f_] = lbl_

        for _, row_data in self.events_df.iterrows():
            mag_ = row_data[self.mandatory_mag_col]
            color_ = "blue"
            if self.color_map:
                color_ = self.color_map(mag_)

            lines = []

            # Magnitude
            if self.mandatory_mag_col in legend_map:
                lines.append(
                    f"<b>{html.escape(legend_map[self.mandatory_mag_col])}</b> {mag_}"
                )
            else:
                lines.append(f"<b>Magnitude:</b> {mag_}")

            # Latitude
            lat_label = legend_map.get("latitude", "Latitude:")
            lines.append(f"<b>{lat_label}</b> {row_data['latitude']:.5f}")

            # Longitude
            lon_label = legend_map.get("longitude", "Longitude:")
            lines.append(f"<b>{lon_label}</b> {row_data['longitude']:.5f}")

            # Possibly add Repi
            if self.show_distance_in_tooltip and "Repi" in row_data:
                dist_km = row_data["Repi"]
                # if user specifically does not want Repi, skip
                # e.g., if there's some additional param "show_distance_in_tooltip=False"
                lines.append(f"<b>Distance:</b> {dist_km:.1f} km")

            # Possibly add ID or other fields from legend
            for field_name, field_label in legend_map.items():
                if field_name in (
                    self.mandatory_mag_col, "latitude", "longitude"
                ):
                    continue
                if field_name in row_data:
                    val_str = str(row_data[field_name]).strip()
                    if val_str.startswith("http://") or val_str.startswith("https://"):
                        link_html = (
                            f'<a href="{html.escape(val_str)}" target="_blank">'
                            f'{html.escape(val_str)}</a>'
                        )
                        lines.append(f"<b>{html.escape(field_label)}</b> {link_html}")
                    else:
                        lines.append(
                            f"<b>{html.escape(field_label)}</b> {html.escape(val_str)}"
                        )

            tooltip_html = "<br>".join(lines)

            radius_ = 4
            if self.event_config.vmin is not None:
                radius_ += (mag_ - self.event_config.vmin) * self.event_config.scaling_factor

            folium.CircleMarker(
                location=[row_data["latitude"], row_data["longitude"]],
                radius=radius_,
                color=color_,
                fill=True,
                fill_opacity=0.7,
                tooltip=tooltip_html
            ).add_to(self.marker_group)

        self.marker_group.add_to(self.map_object)

    def _add_marker_cluster_layer(self):
        """Optional cluster layer if many events."""
        if self.events_df.empty:
            logger.warning("No events to cluster.")
            return

        clus = MarkerCluster(name="Marker Cluster", show=False)
        for _, row_data in self.events_df.iterrows():
            lat_ = row_data["latitude"]
            lon_ = row_data["longitude"]
            mag_ = row_data[self.mandatory_mag_col]
            tip = f"Mag: {mag_:.2f} | ({lat_:.3f}, {lon_:.3f})"
            folium.Marker(location=[lat_, lon_], tooltip=tip).add_to(clus)

        clus.add_to(self.map_object)

    def _add_heatmap_layer(self):
        if self.events_df.empty:
            logger.warning("No events for heatmap.")
            return

        data = [
            (row["latitude"], row["longitude"], row[self.mandatory_mag_col])
            for _, row in self.events_df.iterrows()
        ]
        if not data:
            return

        heat_lay = plugins.HeatMap(
            data=data,
            name="Heatmap",
            min_opacity=self.event_config.heatmap_min_opacity,
            max_zoom=self.map_config.max_zoom_level,
            radius=self.event_config.heatmap_radius,
            blur=self.event_config.heatmap_blur
        )
        fg = folium.FeatureGroup(name="Heatmap", show=False)
        fg.add_child(heat_lay)
        fg.add_to(self.map_object)

    def _add_site_marker(self):
        popup_html = f"""
        <b>Site Project:</b> {self.map_config.project_name}<br>
        <b>Client:</b> {self.map_config.client}
        """
        folium.Marker(
            location=[self.map_config.latitude, self.map_config.longitude],
            icon=folium.Icon(color="red", icon="star", prefix="fa"),
            tooltip=self.map_config.project_name,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(self.map_object)

    def _add_tile_layers(self):
        for layer_name, cfg in TILE_LAYER_CONFIGS.items():
            if layer_name != self.map_config.default_tile_layer:
                folium.TileLayer(
                    tiles=cfg["tiles"],
                    name=layer_name,
                    attr=cfg["attr"],
                    control=True,
                    max_zoom=self.map_config.max_zoom_level,
                    min_zoom=self.map_config.min_zoom_level
                ).add_to(self.map_object)

        default_cfg = TILE_LAYER_CONFIGS[self.map_config.default_tile_layer]
        folium.TileLayer(
            tiles=default_cfg["tiles"],
            name=self.map_config.default_tile_layer,
            attr=default_cfg["attr"],
            control=True,
            max_zoom=self.map_config.max_zoom_level,
            min_zoom=self.map_config.min_zoom_level
        ).add_to(self.map_object)

    def _add_layer_control(self):
        folium.LayerControl().add_to(self.map_object)

    def _add_fullscreen_button(self):
        plugins.Fullscreen(
            position="topleft",
            title="Full Screen",
            title_cancel="Exit Full Screen",
            force_separate_button=True
        ).add_to(self.map_object)

    def _add_color_legend(self):
        if self.color_map is not None:
            self.color_map.position = self.event_config.legend_position.lower()
            self.color_map.add_to(self.map_object)
            logger.info("Color legend added to the map.")
        else:
            logger.info("No color map to add.")

    def _add_faults(self):
        logger.info("Adding fault lines to the map...")
        if self.faults_gdf is None or self.faults_gdf.empty:
            logger.warning("No fault lines to display.")
            return

        style_func = lambda x: {
            "color": self.fault_config.regional_faults_color,
            "weight": self.fault_config.regional_faults_weight,
            "opacity": 1.0
        }
        fault_lyr = folium.GeoJson(
            data=self.faults_gdf,
            style_function=style_func,
            name="Faults",
            show=True
        )
        fault_lyr.add_to(self.map_object)
        logger.info("Fault lines layer added.")

    def _add_stations(self):
        logger.info("Adding stations to the map...")
        if self.stations_df.empty:
            logger.warning("No station data to display.")
            return

        stn_grp = folium.FeatureGroup(
            name=self.station_config.layer_title if self.station_config else "Stations",
            show=True
        )
        icon_map = {
            1: {"color": "blue", "icon": "arrow-up", "prefix": "fa"},
            2: {"color": "green", "icon": "arrows-h", "prefix": "fa"},
            3: {"color": "red", "icon": "cube", "prefix": "fa"}
        }

        for _, row in self.stations_df.iterrows():
            lat_ = row["latitude"]
            lon_ = row["longitude"]
            axes_ = int(row.get("axes", 0))

            icon_conf = icon_map.get(axes_, {
                "color": "gray", "icon": "info-sign", "prefix": "fa"
            })
            tip = (
                f"Station ID: {row.get('ID','?')}<br>"
                f"Type: {row.get('type','N/A')}<br>"
                f"Axes: {axes_}"
            )
            folium.Marker(
                location=[lat_, lon_],
                icon=folium.Icon(
                    color=icon_conf["color"],
                    icon=icon_conf["icon"],
                    prefix=icon_conf["prefix"]
                ),
                tooltip=tip
            ).add_to(stn_grp)

        stn_grp.add_to(self.map_object)
        logger.info("Stations layer added.")

    def _fit_bounds(self):
        """
        Fit the map to self.bounds, then rely on self.map_config.min_zoom_level
        to effectively prevent the user from zooming out further.
        If self.bounds is large, user can see a big area. If it's small, the user sees a small area.
        """
        if not self.bounds:
            logger.warning("No bounding box available. Skipping fit_bounds.")
            return

        logger.info("Fitting map to combined bounds (site + events).")
        self.map_object.fit_bounds(self.bounds, padding=(10, 10))

    def _add_epicentral_distance_layer(self):
        """
        Draw epicentral circles if needed. We'll do fill_opacity=0.0 so
        they don't block markers. Reversing the loop ensures smallest
        circle is drawn last (on top).
        """
        max_distance = self.map_config.radius_km
        circles_count = self.map_config.epicentral_circles
        if circles_count < self.map_config.MIN_EPICENTRAL_CIRCLES:
            circles_count = self.map_config.MIN_EPICENTRAL_CIRCLES
        if circles_count > self.map_config.MAX_EPICENTRAL_CIRCLES:
            circles_count = self.map_config.MAX_EPICENTRAL_CIRCLES

        interval = max_distance / circles_count if circles_count else max_distance
        circ_fg = folium.FeatureGroup(
            name=self.map_config.epicentral_circles_title, show=True
        )

        # **Draw largest circle first -> smallest last**
        for i in reversed(range(1, circles_count + 1)):
            dist_km = i * interval
            radius_m = dist_km * 1000

            folium.Circle(
                location=[self.map_config.latitude, self.map_config.longitude],
                radius=radius_m,
                color="blue",
                fill=True,
                fill_opacity=0.0,  # won't block markers
                weight=1,
                opacity=0.6,
                tooltip=f"{dist_km:.1f} km"
            ).add_to(circ_fg)

            # optional label on boundary
            edge_loc = geodesic(kilometers=dist_km).destination(
                (self.map_config.latitude, self.map_config.longitude),
                0
            )
            folium.Marker(
                location=[edge_loc.latitude, edge_loc.longitude],
                icon=folium.DivIcon(
                    html=f"""
                        <div style='
                            font-size: 12px;
                            color: blue;
                            transform: translate(-50%, -50%);
                            white-space: nowrap;'>
                            {dist_km:.1f} km
                        </div>
                    """
                ),
            ).add_to(circ_fg)

        circ_fg.add_to(self.map_object)
