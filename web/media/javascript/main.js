function post_locate(geolocation_data) {
    if (geolocation_data.latitude != null && geolocation_data.longitude != null) {
        url = '/get_results/'+geolocation_data.latitude+'/'+geolocation_data.longitude
        $('#results').load(url);
        $('#results').show();
    } else {
        $('#unsupported').show();
    }
}

$(document).ready(function(){
        $.geolocator.geolocate({ callback: post_locate});
});