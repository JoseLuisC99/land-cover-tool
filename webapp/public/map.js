function iniciarMap(latitud, longitud){
    var coord = {lat:latitud || -34.5956145 ,lng: longitud || -58.4431949};
    //var coord = {latitud, longitud};
    var map = new google.maps.Map(document.getElementById('map'),{
      zoom: 17,
      center: coord,
      streetViewControl: false,
      mapTypeId: 'satellite',
      zoomControl: false,
      scrollwheel: false,
      mapTypeControl: false,
      fullscreenControl: false,
      styles: [
      {
          "elementType": "labels",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
      {
          featureType: 'transit',
          elementType: 'labels.icon',
          stylers: [{ visibility: 'off' }]
      },
      {
          featureType: 'poi',
          stylers: [{ visibility: 'off' }]
      },
      {
          featureType: 'road',
          stylers: [{ visibility: 'off' }]
      },
  ]
    });
    var marker = new google.maps.Marker({
      position: coord,
      map: map,
      draggable: true,
    });    
}