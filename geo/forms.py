from geo.models import Bookmark
from django.contrib import admin
from django import forms
from django.utils.html import format_html, format_html_join
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.widgets import Textarea


class GoogleEarthWidget(forms.Widget):
    """
    Widget which displays Google Earth Plugin and a textarea widget with current camera kml.
    """

    def _build_js_for_loading_ge(self, textarea_name, element_name, kml, group_name):
        """
        Builds and returns javascript for showing the Google Earth Widget.

        Arguments:
            textarea_name   - name of the textarea field with kml
            element_name    - name of the html tag where Google Earth plugin will be placed
            kml             - initial kml value to fly right after plugin loading
            group_name      - name of the element containing Group name

        Returns:
            Javascript which should be inserted into web page code.
        """
        ge_js_load = """
            <script type="text/javascript">
            var ge;
            var ge_kmlObject;
            var ge_map_type = '';

            google.load("earth", "1");

            function clear_gep() {
              // Clears existing Google Earth Plugin instance.
              document.getElementById('%(element_name)s').innerHTML = '';
              ge_map_type = null;
            }

            function load_earth() {
              // Load Earth data in Google Earth Plugin
              clear_gep();
              google.earth.createInstance('%(element_name)s', initCB, failureCB);
              ge_map_type = 'earth';
            }

            function load_mars() {
              // Load Mars data in Google Earth Plugin
              clear_gep();
              google.earth.createInstance('%(element_name)s', initCB, failureCB, { database: 'http://khmdb.google.com/?db=mars' });
              ge_map_type = 'mars';
            }

            function load_moon() {
              // Load Moon data in Google Earth Plugin
              clear_gep();
              google.earth.createInstance('%(element_name)s', initCB, failureCB, { database: 'http://khmdb.google.com/?db=moon' });
              ge_map_type = 'moon';
            }

            function load_group_map() {
              // Loads map according to current group field.
              var g = document.getElementById('%(group_name)s');
              var group = g.options[g.selectedIndex].text;
              switch (group) {
                case '---------':
                    clear_gep();
                    break;
                case 'earth - Earth':
                    load_earth();
                    break;
                case 'moon - Moon':
                    load_moon();
                    break;
                case 'mars - Mars':
                    load_mars();
                    break;
              }
            }

            function add_group_on_change() {
              // Creates a callback loading proper map data in to Google Earth Plugin
              // when the Group field is changed.
              var g = document.getElementById('%(group_name)s');
              g.onchange=function(){
                document.getElementById('%(textarea_name)s').value = "";
                ge_kmlObject = null;
                load_group_map();
              };
            }

            function init() {
              // The Google Earth Plugin works onlz on Windows or Mac, so I'm hiding it here.
              if (! (navigator.appVersion.indexOf("Win")!=-1 || navigator.appVersion.indexOf("Mac")!=-1)) {
                document.getElementById('%(element_name)s').style.display = "";
                return;
              }

              load_group_map();
              add_group_on_change();
            }

            function initCB(instance) {
              ge = instance;
              ge.getWindow().setVisibility(true);

              if (ge_map_type == 'earth') {
                ge.getLayerRoot().enableLayerById(ge.LAYER_BORDERS, true);
                ge.getLayerRoot().enableLayerById(ge.LAYER_BUILDINGS, true);
                ge.getLayerRoot().enableLayerById(ge.LAYER_ROADS, true);
                ge.getLayerRoot().enableLayerById(ge.LAYER_TERRAIN, true);
                ge.getNavigationControl().setVisibility(ge.VISIBILITY_SHOW);
              }
              ge.getNavigationControl().setVisibility(ge.VISIBILITY_SHOW);
              var kmlString = %(kml)s;
              if (kmlString != '') {
                ge_kmlObject = ge.parseKml(kmlString);
                ge.getFeatures().appendChild(ge_kmlObject);
                if (ge_kmlObject.getAbstractView()) {
                    ge.getView().setAbstractView(ge_kmlObject.getAbstractView());
                }
              }
              google.earth.addEventListener(ge.getView(), 'viewchangeend', function() {
                var view = ge.getView().copyAsLookAt(ge.ALTITUDE_RELATIVE_TO_SEA_FLOOR)
                var kml = "<LookAt>"
                    + "<longitude>"       + view.getLongitude()  + "</longitude>"
                    + "<latitude>"        + view.getLatitude()   + "</latitude>"
                    + "<range>"           + view.getRange()      + "</range>"
                    + "<altitude>"        + view.getAltitude()   + "</altitude>"
                    + "<heading>"         + view.getHeading()    + "</heading>"
                    + "<tilt>"            + view.getTilt()       + "</tilt>"
                    + "<range>"           + view.getRange()      + "</range>"
                    + "<altitudeMode>"    + "relativeToGround"   + "</altitudeMode>"
                    + "<gx:altitudeMode>" + "relativeToSeaFloor" + "</gx:altitudeMode>"
                    + "</LookAt>";
                document.getElementById('%(textarea_name)s').value = kml;
              });
            }

            function failureCB(errorCode) {
            }

            google.setOnLoadCallback(init);
            </script>
        """ % {"element_name": element_name, "kml": kml, 'textarea_name': textarea_name, 'group_name': group_name}

        return mark_safe(ge_js_load)


    def _build_div_for_ge(self, element_name):
        """Returns html tag for placing the Google Earth Plugin in.

        Arguments:
            element_name    - name of the field

        Returns:
            HTML code for inserting into website.
        """
        res = '<span id="%s" style="display: inline-block; height: 300px; width: 800px;"></span>' \
            % element_name
        return mark_safe(res)


    def _build_basic_ge_js(self):
        """
        Returns HTML code for loading the Google Earth Plugin.
        """
        res = '<script type="text/javascript" src="https://www.google.com/jsapi"></script>'
        return mark_safe(res)


    def _build_kml_document(self, kml):
        """
        Builds and returns kml for the initial Google Earth view.

        Arguments:
            kml     -   initial value from textarea field.

        Returns:
            Full KML for loading into Google Earth Plugin.
        """
        res = """
            '<?xml version="1.0" encoding="UTF-8"?>'
            + '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">'
            + '<Document>'
            + '%s'
            + '</Document>'
            + '</kml>'
            """ % kml
        return res


    def _build_ge(self, name, value):
        """
        Builds all the code for Google Earth Widget.

        Arguments:
            name    -   name of the textarea field
            value   -   value of the textarea field

        Returns:
            HTML and Javascript code for Google Earth Widget.
        """
        div_name = "ge_" + name
        group_name = 'id_group'

        kml = self._build_kml_document(value)
        res = [
                self._build_basic_ge_js(),
                self._build_js_for_loading_ge(name, div_name, kml, group_name),
                self._build_div_for_ge(div_name),
              ]

        return " ".join(res)


    def render(self, name, value, attrs=None):

        text_area_widget = Textarea()

        a = None
        ge_attrs = self.build_attrs(a, name="ge_"+name)
        ge = self._build_ge(name, value)
        ge = mark_safe(ge)
        return ge + text_area_widget.render(name, value, {"id": name})


class BookmarkAdminForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        widgets = {
          'flytoview': GoogleEarthWidget
        }

