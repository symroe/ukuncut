function post_locate(geolocation_data) {
    if (geolocation_data.latitude != null && geolocation_data.longitude != null) {
        url = '/get_results/'+geolocation_data.latitude+'/'+geolocation_data.longitude
        $('#results').load(url, function(){$('#loading').hide();});
        $('#results').show();      
    } else {
        $('#unsupported').show();
        $('#loading').hide();        
    }
}

$(document).ready(function(){
        $.geolocator.geolocate({ callback: post_locate});        
        
        $('#postcode_search').bind('click', function() {
            postcode = $('#postcode').attr('value')
            
            if (postcode != '') {
                url = 'http://mapit.mysociety.org/postcode/'+postcode+'?callback=?'
                $('#loading').show();
                $.getJSON(url, function(data) {
                    if (data.error) {
                        $('#loading').hide();
                        // $('<span class="error">'+data.error+'</span>').insertAfter('#postcode');
                        $('#error').html(data.error)
                    } else {
                        url = '/get_results/'+data.wgs84_lat+'/'+data.wgs84_lon;

                        $('#unsupported').hide();

                        $('#results').load(url, function(){$('#loading').hide();});
                        $('#results').show();
                    }
                
                });
            }
            return false;
        })
        
});