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

function change_tab(tab_name){
    if (tab_name == 'results'){
        $('#tab2').show();
        $('#tab1').hide();        
        $('#tab_two').addClass('selected');
        $('#tab_one').removeClass('selected');        
    }else{
        $('#tab1').show();        
        $('#tab2').hide();                
        $('#tab_one').addClass('selected');
        $('#tab_two').removeClass('selected');        
    }
}

function setup_results(){
    //setup geolocation callback
    $.geolocator.geolocate({ callback: post_locate});
    
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
$(document).ready(function(){
    
        //buttons
        $('#tab_one a').click(
            function(){
                change_tab('instructions');
                return false;
            }
        );
        $('#tab_one a').attr('href', '#');
        
        $('#tab_two a').click(
            function(){
                change_tab('results');
                return false;
            }
        );   
        $('#tab_two a').attr('href', '#');        
        
        if ($('#tab1').is(":visible")){
          setup_results();  
        }     
});

