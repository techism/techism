Techism.Map = {}
Techism.Map.attribution = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
Techism.Map.tileUrlHttp = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
Techism.Map.tileUrlHttps = '/map/tile/{z}/{x}/{y}.png';
Techism.Map.tileUrl = location.protocol === 'https:' ? Techism.Map.tileUrlHttps : Techism.Map.tileUrlHttp;
Techism.Map.searchUrlHttp = 'http://nominatim.openstreetmap.org/search';
Techism.Map.searchUrlHttps = '/map/search'
Techism.Map.searchUrl = location.protocol === 'https:' ? Techism.Map.searchUrlHttps : Techism.Map.searchUrlHttp;
Techism.Map.staticUrlHttp = 'http://staticmap.openstreetmap.de/staticmap.php';
Techism.Map.staticUrlHttps = '/map/static'
Techism.Map.staticUrl = location.protocol === 'https:' ? Techism.Map.staticUrlHttps : Techism.Map.staticUrlHttp;


Techism.Map.Map = function() {
    
    this.initializeMunichCityCenter = function() {
        var where = $("#map_canvas");
          var width = where.width();
          var mapId = "map_location";
          var lat = "48.13788";
          var lon = "11.575953";
          if(width < 640) {
              // static map with link for small screens, max. size of static
                // map is 640x640
              var height = Techism.Map.getStaticMapHeight(width);
              where.append('<img id="'+mapId+'" src="'+Techism.Map.staticUrl+'?center='+lat+','+lon+'&zoom=15&size='+width+'x'+height+'" />');
          }
          else {
              // dynamic map for larger screens
              var height = Techism.Map.getDynamicMapHeight(width);
              where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
              this.map = L.map(mapId, {
                  scrollWheelZoom: false
              }).setView([lat, lon], 17);
              L.tileLayer(Techism.Map.tileUrl, {
                  attribution: Techism.Map.attribution,
                  maxZoom: 18
              }).addTo(this.map);
          }
    };

    this.displayLocation = function(name, street, city, lat, lng) {
        if (street.length > 0 && city.length > 0){
            var where = $("#map_location");
            var location = street +","+city
            var thisMap = this;
            $.getJSON(Techism.Map.searchUrl + "?q=" + encodeURIComponent(location) + "&format=json&polygon=1,limit=1", {}, function (data){
                if(data[0]) {
                    var loc = data[0]
                    if (where[0] && where[0].nodeName && where[0].nodeName == "DIV"){
                        thisMap.map.setView([loc.lat, loc.lon], 17);
                        if(!thisMap.marker) {
                            thisMap.marker = L.marker([loc.lat, loc.lon]).addTo(thisMap.map);
                        }
                        else {
                            thisMap.marker.setLatLng([loc.lat, loc.lon]);
                        }
                    } 
                    else {
                        // img of #map_location may not yet be loaded, use
                        // parent
                        var width = where.parent().width(); 
                        var height = Techism.Map.getStaticMapHeight(width);
                        var newMap = '<img id="map_location" src="'+Techism.Map.staticUrl+'?center='+loc.lat+','+loc.lon+'&zoom=15&size='+width+'x'+height+'&markers='+loc.lat+','+loc.lon+',ol-marker" />';
                        where.replaceWith(newMap);
                    }
                }
            });
        }
    }
}


Techism.Map.renderEventDetailMap = function() {
    var where = $(this).children("section.where");
    
    // exit if no where id exists
    if( where.length == 0) {
        return;
    }
    
    // the id of that map div
    var mapId = "map_" + where[0].id;
    
    // only load the map once
    if( $("#"+mapId).length > 0) {
        return;
    }
    
    // get the map link
    var mapLink = where.find('a')
    
    // exit if there isn't a map link
    if( mapLink.length == 0) {
        return;
    }
    
    // extract query string and 'mlat' and 'mlon' parameters from link
    var query = Techism.Map.parseQuery(mapLink[0].search, {'f':function(v){return v;}})
    var lat = query.mlat;
    var lon = query.mlon

    var width = where.width();
    var height = Math.round(width / 2);
    if(width < 640) {
        // static map with link for small screens, max. size of static map is
        // 640x640
        var height = Techism.Map.getStaticMapHeight(width);
        where.append('<img src="'+Techism.Map.staticUrl+'?center='+lat+','+lon+'&zoom=15&size='+width+'x'+height+'&markers='+lat+','+lon+',ol-marker" />');
    }
    else {
        // dynamic map for larger screens
        var height = Techism.Map.getDynamicMapHeight(width);
        where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
        var map = L.map(mapId, {
            scrollWheelZoom: false
        }).setView([lat, lon], 17);
        L.tileLayer(Techism.Map.tileUrl, {
            attribution: Techism.Map.attribution,
            maxZoom: 18
        }).addTo(map);
        var marker = L.marker([lat, lon]).addTo(map);
    }
};

// utility methods
Techism.Map.parseQuery = function(qs,options) {
    var q = (typeof qs === 'string'?qs:window.location.search), o = {'f':function(v){return unescape(v).replace(/\+/g,' ');}}, options = (typeof qs === 'object' && typeof options === 'undefined')?qs:options, o = jQuery.extend({}, o, options), params = {};
    jQuery.each(q.match(/^\??(.*)$/)[1].split('&'),function(i,p){
        p = p.split('=');
        p[1] = o.f(p[1]);
        params[p[0]] = params[p[0]]?((params[p[0]] instanceof Array)?(params[p[0]].push(p[1]),params[p[0]]):[params[p[0]],p[1]]):p[1];
    });
    return params;
};

Techism.Map.getDynamicMapHeight = function(width){
    return Math.round(width / 3)
};

Techism.Map.getStaticMapHeight = function(width){
    return Math.round(width / 2)
};
