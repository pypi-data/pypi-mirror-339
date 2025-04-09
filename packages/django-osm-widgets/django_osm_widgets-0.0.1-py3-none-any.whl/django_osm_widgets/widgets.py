# Django
from django.contrib.gis.forms import OSMWidget


class LatLonOpenlayersOSMWidget(OSMWidget):
    """
    A widget that displays an OSM map and two input fields for latitude and
    longitude.
    Updating the point on the map will update the latitude and longitude fields
    and updating the fields will update the point on the map.
    """

    must_display_latlon_fields = True
    template_name = "django_osm_widgets/latlon-openlayers-osm.html"

    class Media(OSMWidget.Media):
        js = OSMWidget.Media.js + ("django_osm_widgets/LatLonOpenlayersOSMWidget.js",)

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs["must_display_latlon_fields"] = self.must_display_latlon_fields
        if attrs:
            self.attrs.update(attrs)
