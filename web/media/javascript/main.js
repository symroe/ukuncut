var geo_location = new Object();

function post_locate_targets(geolocation_data) {
    
    if (geolocation_data.latitude != null && geolocation_data.longitude != null) {
        geo_location = geolocation_data;
        
        url = '/get_results/'+geolocation_data.latitude+'/'+geolocation_data.longitude;
        $('#results').load(url, function(){$('#loading').hide();});
        $('#results').show();      
    } else {
        $('#unsupported').show();
        $('#loading').hide();        
    }
}

function post_locate_events(geolocation_data) {
    if (geolocation_data.latitude != null && geolocation_data.longitude != null) {
        url = '/get_events/'+geolocation_data.latitude+'/'+geolocation_data.longitude;
        $('#events').load(url, function(){$('#loading').hide();});
        $('#events').show();      
    } else {
        $('#unsupported').show();
        $('#loading').hide();        
    }
}

function change_tab(tab_name){
    $('#results').html('');
    $('#events').html('');
    if (tab_name == 'results'){
        $('#tab1').show();
        $('#tab2').hide();
        $('#tab3').hide();                
        $('#tab_one').addClass('selected');
        $('#tab_two').removeClass('selected');        
        $('#tab_three').removeClass('selected');    
    }else if (tab_name == 'events'){
        $('#tab1').hide();
        $('#tab2').show();
        $('#tab3').hide();
        $('#tab_one').removeClass('selected');
        $('#tab_two').addClass('selected');        
        $('#tab_three').removeClass('selected');                            
    }else{
        $('#tab1').hide();
        $('#tab2').hide();
        $('#tab3').show();                
        $('#tab_one').removeClass('selected');
        $('#tab_two').removeClass('selected');        
        $('#tab_three').addClass('selected');
        
        $('#unsupported').hide();
        $('#loading').hide();
    }
}

function setup_targets(){

    //setup geolocation callback
    if (geo_location.longitude == null) {
        $.geolocator.geolocate({ callback: post_locate_targets});
    } else {
        post_locate_targets(geo_location)
    }
    
    $('#unsupported').hide();
    $('#loading').show();
    
    //Setup postcode fallback
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
                    
                    geo_location.latitude = data.wgs84_lat
                    geo_location.longitude = data.wgs84_lon
                    
                    url = '/get_results/'+data.wgs84_lat+'/'+data.wgs84_lon;

                    $('#unsupported').hide();

                    $('#results').load(url, function(){$('#loading').hide();});
                    $('#results').show();
                }
            
            });
        }
        return false;
    })   
}

function setup_events(){
    //setup geolocation callback
    if (geo_location.latitude == null) {
        $.geolocator.geolocate({ callback: post_locate_events});
    } else {
        post_locate_events(geo_location)
    }

    $('#unsupported').hide();
    $('#loading').show();
}

$(document).ready(function(){
    
        //buttons
        $('#tab_one a').attr('href', '#');        
        $('#tab_two a').attr('href', '#');        
        $('#tab_three a').attr('href', '#');                
                
        $('#tab_one a').click(
            function(){
                change_tab('results');
                setup_targets();                
                return false;
            }
        );
        
        $('#tab_two a').click(
            function(){
                change_tab('events');
                setup_events();
                return false;
            }
        );
        
        $('#tab_three a').click(
            function(){
                change_tab('instructions');
                return false;
            }
        );
        
        //default tab
        $('#tab_one a').click();
        
        //setup iphone bookmark prompt
        window.addEventListener('load', function() {
          window.setTimeout(function() {
            var bubble = new google.bookmarkbubble.Bubble();

            var parameter = 'bmb=1';

            bubble.hasHashParameter = function() {
              return window.location.hash.indexOf(parameter) != -1;
            };

            bubble.setHashParameter = function() {
              if (!this.hasHashParameter()) {
                window.location.hash += parameter;
              }
            };

            bubble.getViewportHeight = function() {
              window.console.log('Example of how to override getViewportHeight.');
              return window.innerHeight;
            };

            bubble.getViewportScrollY = function() {
              window.console.log('Example of how to override getViewportScrollY.');
              return window.pageYOffset;
            };

            bubble.registerScrollHandler = function(handler) {
              window.console.log('Example of how to override registerScrollHandler.');
              window.addEventListener('scroll', handler, false);
            };

            bubble.deregisterScrollHandler = function(handler) {
              window.console.log('Example of how to override deregisterScrollHandler.');
              window.removeEventListener('scroll', handler, false);
            };

            bubble.showIfAllowed();
          }, 1000);
        }, false);
    
});

