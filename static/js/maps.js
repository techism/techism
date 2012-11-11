function renderEventDetailMap() {
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
	var query = $.parseQuery(mapLink[0].search, {'f':function(v){return v;}})
	var lat = query.mlat;
	var lon = query.mlon
	
	var width = where.width();
	var height = Math.round(width / 2);
	if(width < 640) {
		// static map with link for small screens, max. size of static map is 640x640
		var height = getStaticMapHeight(width);
		where.append('<img src="http://staticmap.openstreetmap.de/staticmap.php?center='+lat+','+lon+'&zoom=15&size='+width+'x'+height+'&markers='+lat+','+lon+',ol-marker" />');
	}
	else {
		// dynamic map for larger screens
		var height = getDynamicMapHeight(width);
		where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
		var map = L.map(mapId).setView([lat, lon], 17);
		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		    attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
		    maxZoom: 18
		}).addTo(map);
		var marker = L.marker([lat, lon]).addTo(map);
	}
}

// utility methods

jQuery.parseQuery = function(qs,options) {
	var q = (typeof qs === 'string'?qs:window.location.search), o = {'f':function(v){return unescape(v).replace(/\+/g,' ');}}, options = (typeof qs === 'object' && typeof options === 'undefined')?qs:options, o = jQuery.extend({}, o, options), params = {};
	jQuery.each(q.match(/^\??(.*)$/)[1].split('&'),function(i,p){
		p = p.split('=');
		p[1] = o.f(p[1]);
		params[p[0]] = params[p[0]]?((params[p[0]] instanceof Array)?(params[p[0]].push(p[1]),params[p[0]]):[params[p[0]],p[1]]):p[1];
	});
	return params;
}

function getDynamicMapHeight(width){
  return Math.round(width / 3)
}

function getStaticMapHeight(width){
  return Math.round(width / 2)
}
