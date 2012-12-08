$(function() {
    $.datepicker.setDefaults($.datepicker.regional["de"]);
    $("#id_date_time_begin_0").datepicker($.datepicker.regional["de"]);
    $("#id_date_time_end_0").datepicker($.datepicker.regional["de"]);

    // load locations via AJAX, add 'label' for auto completion
    var availableLocs = [];
    $.getJSON("/events/locations/", {
        ajax : 'true'
    }, function(jsonLocation) {
        jsonLocation.map(function(item) {
            item.label = item.name + ', ' + item.street + ', ' + item.city;
            availableLocs.push(item);
        });
    });

    // activate auto completion for location
    $("#id_location_name").autocomplete({
        source : availableLocs,
        select : function(event, ui) {
            $("#id_location_name").val(ui.item.name);
            $("#id_location_street").val(ui.item.street);
            $("#id_location_city").val(ui.item.city);
            $("#id_location").val(ui.item.id);
            return false;
        }
    });

    // show the map
    var map = new Techism.Map.Map();
    map.initializeMunichCityCenter();

    // show coordinates in map
    $("#id_location_show_in_map").click(function() {
        var name = $("#id_location_name").val();
        var street = $("#id_location_street").val();
        var city = $("#id_location_city").val();
        // var lat = $("#id_location_lat").val();
        // var lon = $("#id_location_lon").val();

        map.displayLocation(name, street, city);
    });
});