class LatLonOpenlayersOSMWidget {
  _canUpdateLatLonFields = true;

  constructor(options) {
      // Default options
    this.options = {
      mapWidgetInstance: null,
      latitudeFieldId: 'id_osm_widget_latitude',
      longitudeFieldId: 'id_osm_widget_longitude',
      listenedEvents: 'input',
      locale: navigator.language || 'en-GB',
      markerOptions: {
        src: '/static/django_osm_widgets/marker.svg',
        scale: 1.5,
        anchor: [0.5, 1],
      },
    };

      // Altering using user-provided options
    for (const property in options) {
      if (options.hasOwnProperty(property)) {
        this.options[property] = options[property];
      }
    }

    this.map = this.options.mapWidgetInstance.map;

    this.latitudeField = document.getElementById(this.options.latitudeFieldId);
    this.longitudeField = document.getElementById(this.options.longitudeFieldId);
    this.latitudeField.addEventListener(this.options.listenedEvents, this.updateMap.bind(this));
    this.longitudeField.addEventListener(this.options.listenedEvents, this.updateMap.bind(this));

    const styles = [
      new ol.style.Style({
        image: new ol.style.Icon(this.options.markerOptions),
      }),
    ];
    this.options.mapWidgetInstance.featureOverlay.setStyle(styles);

    this.options.mapWidgetInstance.featureCollection.on('add',  function(event) {
      const feature = event.element;
      this.updateLatLonFields(feature);
      feature.on('change', function(event) { this.updateLatLonFields(feature); }.bind(this));
    }.bind(this));
  }

  debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
  }

  centerMap = this.debounce((coordinates) => this.map.getView().setCenter(coordinates), 500);

  cleanCoordinates(coordinate) {
    return coordinate.replace(',', '.').replace(' ', '');
  }

  isCoordinatesValid(latitude, longitude) {
      // Latitude/longitude are valid numbers
    if (!latitude.match(/^-?\d+(\.\d+)?$/) || !longitude.match(/^-?\d+(\.\d+)?$/)) {
      return false;
    }

      // Check if latitude is between -90 and 90 degrees
    if (latitude < -90 || latitude > 90) {
      return false;
    }

      // Check if longitude is between -180 and 180 degrees
    if (longitude < -180 || longitude > 180) {
      return false;
    }

    return true;
  }

  getCoordinatesFromFields() {
    const latitude_str = this.cleanCoordinates(this.latitudeField.value);
    const longitude_str = this.cleanCoordinates(this.longitudeField.value);

    if (!this.isCoordinatesValid(latitude_str, longitude_str)) {
      return;
    }

    return ol.proj.transform([longitude_str, latitude_str], 'EPSG:4326', this.map.getView().getProjection());
  }

  updateMap() {
      // Update the feature on the map when the lat/lon fields are modified
    const center = this.getCoordinatesFromFields();

    if (!center) {
      return;
    }

      // Stop updating the lat/lon fields to avoid infinite loop
    this._canUpdateLatLonFields = false;

    this.map.getView().setCenter(center);

    this.options.mapWidgetInstance.clearFeatures();

    const jsonFormat = new ol.format.GeoJSON();
    const features = jsonFormat.readFeatures('{"type": "Feature", "geometry": {"type":"Point","coordinates":[' + center + ']}}');
    const extent = ol.extent.createEmpty();
    features.forEach(function(feature) {
      this.featureOverlay.getSource().addFeature(feature);
      ol.extent.extend(extent, feature.getGeometry().getExtent());
    }, this.options.mapWidgetInstance);

      // Center/zoom the map
    this.map.getView().fit(extent, {minResolution: 1});

      // Allow updating the lat/lon fields again
    this._canUpdateLatLonFields = true;
  }

  updateLatLonFields(feature) {
      // Update the lat/lon fields when a feature is added or modified

      // We handle only single feature
    if (!this.options.mapWidgetInstance.is_collection) {
      const coordinates = feature.getGeometry().getCoordinates();
      const transformedCoordinates = ol.proj.transform(coordinates, this.map.getView().getProjection(), 'EPSG:4326');

      this.centerMap(coordinates);

        // Avoid infinite loop
      if (this._canUpdateLatLonFields) {
        this.latitudeField.value = transformedCoordinates[1].toLocaleString(this.options.locale, { maximumSignificantDigits: 15 });
        this.longitudeField.value = transformedCoordinates[0].toLocaleString(this.options.locale, { maximumSignificantDigits: 15 });
      }
    }
  }
}

