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