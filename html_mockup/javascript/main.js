
function locate(){
    if ($.geolocation.support()){
        $.geolocation.find(function(location){
           alert(location.latitude+", "+location.longitude);
           $('#results').show();
        });
    }else{
        $('#unsupported').show();
    }
}