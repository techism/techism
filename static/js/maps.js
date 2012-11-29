
Techism.Map = {}
Techism.Map.attribution = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
Techism.Map.tileUrlHttp = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
Techism.Map.tileUrlHttps = '/tile/{z}/{x}/{y}.png';
Techism.Map.tileUrl = location.protocol === 'https:' ? Techism.Map.tileUrlHttps : Techism.Map.tileUrlHttp;


function displayLocation(street, city){
  var where = $("#map_location");
  var location = street +","+city+","+ "Bayern";
  if (where[0].nodeName == "DIV"){
    if (street.length > 0 && city.length > 0){
        deleteOverlays();
        geocodeAndSetMarker (map, location, true);
    }
  } else {
    var width = where.parent().width(); // img of #map_location may not yet be loaded, use parent
    var height = Techism.Map.getStaticMapHeight(width);
    var newMap = '<img id="map_location" src="http://maps.google.com/maps/api/staticmap?center=' + location + '&size='+width+'x'+height+'&zoom=15&sensor=false&markers=color:red|' + location + '" />';
    where.replaceWith(newMap);
  }
}


function initializeMunichCityCenter() {
  var where = $("#map_canvas");
  var width = where.width();
  var mapId = "map_location";
  //if(width < 640) {
    // static map with link for small screens, max. size of static map is 640x640
    var height = Techism.Map.getStaticMapHeight(width);
    var lat = "48.13788";
    var lon = "11.575953";
    where.append('<img src="http://staticmap.openstreetmap.de/staticmap.php?center='+lat+','+lon+'&zoom=15&size='+width+'x'+height+'" />');
  //}
  //else {
    // dynamic map for larger screens
  //  var height = getDynamicMapHeight(width);
  //  where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
  //  var myOptions = getOptionsMunichCityCenter ();
  //  map = new google.maps.Map(document.getElementById(mapId), myOptions);
  //}
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
		// static map with link for small screens, max. size of static map is 640x640
		var height = Techism.Map.getStaticMapHeight(width);
		where.append('<img src="http://staticmap.openstreetmap.de/staticmap.php?center='+lat+','+lon+'&zoom=15&size='+width+'x'+height+'&markers='+lat+','+lon+',ol-marker" />');
	}
	else {
		// dynamic map for larger screens
		var height = Techism.Map.getDynamicMapHeight(width);
		where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
		var map = L.map(mapId).setView([lat, lon], 17);
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
}

Techism.Map.getDynamicMapHeight = function(width){
  return Math.round(width / 3)
}

Techism.Map.getStaticMapHeight = function(width){
  return Math.round(width / 2)
}
