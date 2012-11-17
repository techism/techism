var geocoder;
var map;
var locations;

	initializeMunichCityCenter();


$(function() {
	$.datepicker.setDefaults( $.datepicker.regional[ "de" ] );
	$("#id_date_time_begin_0").datepicker( $.datepicker.regional[ "de" ]);
	$("#id_date_time_end_0").datepicker( $.datepicker.regional[ "de" ]);
});