// Default infoBox Rating Type
var infoBox_ratingType = 'star-rating';

(function ($) {
    "use strict";

    function mainMap() {

        // Locations
        // ----------------------------------------------- //
        var ib = new InfoBox();

        // Infobox Output
        function locationData(locationURL, locationImg, locationTitle, locationAddress, locationRating, locationRatingCounter) {
            return [locationURL, locationImg, locationTitle, locationAddress, locationRating, locationRatingCounter]
        }

        function lolo(loData, facarray) {
            console.log(JSON.parse(loData));
            var jl = JSON.parse(loData)
            var html = ('' +
                '<a href="listings-single/' + jl[0].place_ID + '" class="listing-img-container">' +
                '<div class="infoBox-close"><i class="fa fa-times"></i></div>' +
                '<img src="' + '/static/images/listing-item-01.jpg' + '" alt="">' +

                '<div class="listing-item-content">');

            for (var i = 0; i < facarray.length; i++) {
                html += '<h4 style="color:orangered">' + facarray[i] + '</h4>';
            }


            html += ('<h3>' + jl[0].place_name + '</h3>' +
                '<span>' + jl[0].place_address + '</span>' +
                '</div>' +

                '</a>' +

                '<div class="listing-content">' +
                '<div class="listing-title">' +
                '</div>' +
                '</div>');

            return html
        }

        var datacomeonplease = $('#map').attr('dd');

        var wishgohome = JSON.parse(datacomeonplease);


        var locations2 = new Array();

        for (i = 0; i < wishgohome.length; i++) {
            locations2.push([locationData('listings-single/' + wishgohome[i].place_ID, '/static/images/listing-item-01.jpg', wishgohome[i].place_name, wishgohome[i].place_address, '4.0', '10'), wishgohome[i].lat, wishgohome[i].lng, i, '<i class="im im-icon-Chef-Hat"></i>', wishgohome[i].place_ID]);
        }

        // Chosen Rating Type
        google.maps.event.addListener(ib, 'domready', function () {
            if (infoBox_ratingType = 'numerical-rating') {
                numericalRating('.infoBox .' + infoBox_ratingType + '');
            }
            if (infoBox_ratingType = 'star-rating') {
                starRating('.infoBox .' + infoBox_ratingType + '');
            }
        });


        // Map Attributes
        // ----------------------------------------------- //

        var mapZoomAttr = $('#map').attr('data-map-zoom');
        console.log(mapZoomAttr);
        var mapScrollAttr = $('#map').attr('data-map-scroll');


        if (typeof mapZoomAttr !== typeof undefined && mapZoomAttr !== false) {
            var zoomLevel = parseInt(mapZoomAttr);
        } else {
            var zoomLevel = 5;
        }

        if (typeof mapScrollAttr !== typeof undefined && mapScrollAttr !== false) {
            var scrollEnabled = parseInt(mapScrollAttr);
        } else {
            var scrollEnabled = false;
        }


        // Main Map
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: zoomLevel,
            scrollwheel: scrollEnabled,
            isfind: false,
            center: new google.maps.LatLng(37.5, 127.0),
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoomControl: false,
            mapTypeControl: false,
            scaleControl: false,
            panControl: false,
            navigationControl: false,
            streetViewControl: false,
            gestureHandling: 'cooperative',

            // Google Map Style
            styles: [{
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#747474"}, {"lightness": "23"}]
            }, {
                "featureType": "poi.attraction",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#f38eb0"}]
            }, {
                "featureType": "poi.government",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ced7db"}]
            }, {
                "featureType": "poi.medical",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ffa5a8"}]
            }, {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#c7e5c8"}]
            }, {
                "featureType": "poi.place_of_worship",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#d6cbc7"}]
            }, {
                "featureType": "poi.school",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#c4c9e8"}]
            }, {
                "featureType": "poi.sports_complex",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#b1eaf1"}]
            }, {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [{"lightness": "100"}]
            }, {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [{"visibility": "off"}, {"lightness": "100"}]
            }, {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ffd4a5"}]
            }, {
                "featureType": "road.arterial",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ffe9d2"}]
            }, {
                "featureType": "road.local",
                "elementType": "all",
                "stylers": [{"visibility": "simplified"}]
            }, {
                "featureType": "road.local",
                "elementType": "geometry.fill",
                "stylers": [{"weight": "3.00"}]
            }, {
                "featureType": "road.local",
                "elementType": "geometry.stroke",
                "stylers": [{"weight": "0.30"}]
            }, {
                "featureType": "road.local",
                "elementType": "labels.text",
                "stylers": [{"visibility": "on"}]
            }, {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#747474"}, {"lightness": "36"}]
            }, {
                "featureType": "road.local",
                "elementType": "labels.text.stroke",
                "stylers": [{"color": "#e9e5dc"}, {"lightness": "30"}]
            }, {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [{"visibility": "on"}, {"lightness": "100"}]
            }, {"featureType": "water", "elementType": "all", "stylers": [{"color": "#d2e7f7"}]}]

        });


        // Marker highlighting when hovering listing item
        $('.listing-item-container').on('mouseover', function () {

            var listingAttr = $(this).data('marker-id');

            if (listingAttr !== undefined) {
                var listing_id = $(this).data('marker-id') - 1;
                var marker_div = allMarkers[listing_id].div;

                $(marker_div).addClass('clicked');

                $(this).on('mouseout', function () {
                    if ($(marker_div).is(":not(.infoBox-opened)")) {
                        $(marker_div).removeClass('clicked');
                    }
                });
            }

        });


        // Infobox
        // ----------------------------------------------- //

        var boxText = document.createElement("div");
        boxText.className = 'map-box'

        var currentInfobox;

        var boxOptions = {
            content: boxText,
            disableAutoPan: false,
            alignBottom: true,
            maxWidth: 0,
            pixelOffset: new google.maps.Size(-134, -55),
            zIndex: null,
            boxStyle: {
                width: "270px"
            },
            closeBoxMargin: "0",
            closeBoxURL: "",
            infoBoxClearance: new google.maps.Size(35, 25),
            isHidden: false,
            pane: "floatPane",
            enableEventPropagation: false,
        };


        var markerCluster, overlay, i;
        var allMarkers = [];

        var clusterStyles = [
            {
                textColor: 'white',
                url: '',
                height: 50,
                width: 50
            }
        ];


        var markerIco;
        for (i = 0; i < locations2.length; i++) {

            markerIco = locations2[i][4];

            var overlaypositions = new google.maps.LatLng(locations2[i][1], locations2[i][2]),

                overlay = new CustomMarker(
                    overlaypositions,
                    map,
                    {
                        marker_id: i
                    },
                    markerIco
                );

            allMarkers.push(overlay);

            google.maps.event.addDomListener(overlay, 'click', (function (overlay, i) {

                return function () {
                    ib.setOptions(boxOptions);
                    $.getJSON('/getData', {
                        a: locations2[i][5]
                    }, function (data) {
                        var jd = JSON.parse(data[1]);
                        console.log(jd);
                        var fay = [];
                        for (var i = 0; i < jd.length; i++) {
                            fay.push(jd[i].facility_available_name);
                        }
                        console.log("fay : "+fay);
                        boxText.innerHTML = lolo(data[0], fay);
                        ib.close();
                        ib.open(map, overlay);
                        currentInfobox = data[0].place_id;
                    });


                    // var latLng = new google.maps.LatLng(locations[i][1], locations[i][2]);
                    // map.panTo(latLng);
                    // map.panBy(0,-90);


                    google.maps.event.addListener(ib, 'domready', function () {
                        $('.infoBox-close').click(function (e) {
                            e.preventDefault();
                            ib.close();
                            $('.map-marker-container').removeClass('clicked infoBox-opened');
                        });

                    });

                }
            })(overlay, i));

        }


        // Marker Clusterer Init
        // ----------------------------------------------- //

        var options = {
            imagePath: '/static/images/',
            styles: clusterStyles,
            minClusterSize: 2
        };

        markerCluster = new MarkerClusterer(map, allMarkers, options);

        google.maps.event.addDomListener(window, "resize", function () {
            var center = map.getCenter();
            google.maps.event.trigger(map, "resize");
            map.setCenter(center);
        });


        // Custom User Interface Elements
        // ----------------------------------------------- //

        // Custom Zoom-In and Zoom-Out Buttons
        var zoomControlDiv = document.createElement('div');
        var zoomControl = new ZoomControl(zoomControlDiv, map);

        function ZoomControl(controlDiv, map) {

            zoomControlDiv.index = 1;
            map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(zoomControlDiv);
            // Creating divs & styles for custom zoom control
            controlDiv.style.padding = '5px';
            controlDiv.className = "zoomControlWrapper";

            // Set CSS for the control wrapper
            var controlWrapper = document.createElement('div');
            controlDiv.appendChild(controlWrapper);

            // Set CSS for the zoomIn
            var zoomInButton = document.createElement('div');
            zoomInButton.className = "custom-zoom-in";
            controlWrapper.appendChild(zoomInButton);

            // Set CSS for the zoomOut
            var zoomOutButton = document.createElement('div');
            zoomOutButton.className = "custom-zoom-out";
            controlWrapper.appendChild(zoomOutButton);

            // Setup the click event listener - zoomIn
            google.maps.event.addDomListener(zoomInButton, 'click', function () {
                map.setZoom(map.getZoom() + 1);
            });

            // Setup the click event listener - zoomOut
            google.maps.event.addDomListener(zoomOutButton, 'click', function () {
                map.setZoom(map.getZoom() - 1);
            });

        }


        // Scroll enabling button
        var scrollEnabling = $('#scrollEnabling');

        $(scrollEnabling).click(function (e) {
            e.preventDefault();
            $(this).toggleClass("enabled");

            if ($(this).is(".enabled")) {
                map.setOptions({'scrollwheel': true});
            } else {
                map.setOptions({'scrollwheel': false});
            }
        })


        // Geo Location Button
        $("#geoLocation, .input-with-icon.location a").click(function (e) {
            e.preventDefault();
            geolocate();
        });

        function geolocate() {

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                    map.setCenter(pos);

                    addMarker(pos, map);
                    map.setZoom(17);
                });
            }
        }

        var setfind = $("#gonnafind");
        $(setfind).click(function (e) {
            e.preventDefault();
            $(this).toggleClass("enabled");

            if ($(this).is(".enabled")) {
                map.setOptions({'isfind': true});
            } else {
                map.setOptions({'isfind': false});
            }
            map.addListener('click', function (e) {
                if (map.get('isfind')) {
                    addMarker(e.latLng, map);
                    showMarkers(map);
                } else {
                    deleteMarkers(map);
                }
            });
        });

        var geocoder = new google.maps.Geocoder();
         document.getElementById('submit').addEventListener('click', function() {
          geocodeAddress(geocoder, map);
        });
    }

    function geocodeAddress(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            resultsMap.setZoom(17);
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });
      }

    var markers = [];
    // Map Init
    var map = document.getElementById('map');
    if (typeof(map) != 'undefined' && map != null) {
        google.maps.event.addDomListener(window, 'load', mainMap);

    }


    var recommendMarker = [];

    function addMarker(location, map) {
        var marker = new google.maps.Marker({
            position: location,
            map: map
        });
        markers.push(marker);
        getCheckValue();


        //     var form = document.createElement("form");
        //     form.setAttribute("method", "post");
        //     form.setAttribute("action", "/listing");
        //
        //     var hiddenField1 = document.createElement("input");
        //     hiddenField1.setAttribute("type", "hidden");
        //     hiddenField1.setAttribute("name", "lat");
        //     hiddenField1.setAttribute("value", location.lat());
        //     console.log(hiddenField1.lat);
        //     form.appendChild(hiddenField1);
        //
        //     var hiddenField2 = document.createElement("input");
        //     hiddenField2.setAttribute("type", "hidden");
        //     hiddenField2.setAttribute("name", 'lng');
        //     hiddenField2.setAttribute("value", location.lng());
        //     form.appendChild(hiddenField2);
        //
        //
        //     document.body.appendChild(form);
        //     form.submit();
        // }
        //     console.log(JSON.stringify({'lat':location.lat, 'lng':location.lng}));
        $.ajax({
            url: '/getCF',
            type: 'POST',
            data: {'lat': location.lat, 'lng': location.lng, 'selectedfac': getCheckValue},
            dataType: 'json',
            success: function (data) {
                // console.log("ss" + data[0].lat);

                for (var i = 0; i < 5; i++) {
                    (function (i) {
                        // console.log("ddd" + data[i].lat);

                        var cor1 = data[i].lat;
                        var cor2 = data[i].lng;

                        var itemlist = document.getElementById('itemlist-' + i);
                        itemlist.onclick = function () {
                            var center = new google.maps.LatLng(cor1, cor2);
                            map.panTo(center);
                        }
                        itemlist.innerHTML = "<div class=\"listing-item\">\n" +
                            "                                <!-- Image -->\n" +
                            "                                <div class=\"listing-item-image\">\n" +
                            "                                    <img src=\"images/listing-item-01.jpg\" alt=\"\">\n" +
                            "                                    <span class=\"tag\">" + data[i].category + "</span>\n" +
                            "                                </div>\n" +
                            "\n" +
                            "                                <!-- Content -->\n" +
                            "                                <div class=\"listing-item-content\">\n" +
                            "                                    <div class=\"listing-item-inner\">\n" +
                            "                                        <h3>" + data[i].place_name + " <i class=\"verified-icon\"></i></h3>\n" +
                            "                                        <span>" + data[i].place_address + "</span>\n" +
                            "                                        <div class=\"star-rating\" data-rating=\"3.5\">\n" +
                            "                                            <div class=\"rating-counter\">(12 reviews)</div>\n" +
                            "                                        </div>\n" +
                            "                                    </div>\n" +
                            "\n" +
                            "                                    <span class=\"like-icon\"></span>\n" +
                            "                                </div>\n" +
                            "                            </div>"
                    })(i);

                }


                // for (var i = 0; i < data.length; i++) {
                //     recommendMarker.push(new google.maps.Marker({
                //         position: new google.maps.LatLng(data[i].lat, data[i].lng),
                //         map: map
                //     }));
                // }
                alert("추천 목록 확인하세요");
            },
            error: function (er) {
                alert("error " + er.status);
                console.log("er" + er);
            }

        })
    }

    function setMapOnAll(map) {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
        }
        for (var i = 0; i < recommendMarker.length; i++) {
            recommendMarker[i].setMap(map);
        }

    }

    function clearMarkers(map) {
        setMapOnAll(null);
    }

    function showMarkers(map) {
        setMapOnAll(map);
    }

    function deleteMarkers(map) {
        clearMarkers(map);
        markers = [];
        recommendMarker = [];
    }

    function getCheckValue() {
        var check = document.getElementsByName('check');
        var checkvalue = [];

        for (var i = 0; i < check.length; i++) {
            if (check[i].checked) {
                checkvalue.push(i);
            }
        }
        console.log("checkvalue : "+checkvalue);
        return checkvalue;
    }


    // ---------------- Main Map / End ---------------- //


    // Single Listing Map
    // ----------------------------------------------- //

    function singleListingMap() {

        var myLatlng = new google.maps.LatLng({
            lng: $('#singleListingMap').data('longitude'),
            lat: $('#singleListingMap').data('latitude'),
        });

        var single_map = new google.maps.Map(document.getElementById('singleListingMap'), {
            zoom: 15,
            center: myLatlng,
            scrollwheel: false,
            zoomControl: false,
            mapTypeControl: false,
            scaleControl: false,
            panControl: false,
            navigationControl: false,
            streetViewControl: false,
            styles: [{
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#747474"}, {"lightness": "23"}]
            }, {
                "featureType": "poi.attraction",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#f38eb0"}]
            }, {
                "featureType": "poi.government",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ced7db"}]
            }, {
                "featureType": "poi.medical",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ffa5a8"}]
            }, {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#c7e5c8"}]
            }, {
                "featureType": "poi.place_of_worship",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#d6cbc7"}]
            }, {
                "featureType": "poi.school",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#c4c9e8"}]
            }, {
                "featureType": "poi.sports_complex",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#b1eaf1"}]
            }, {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [{"lightness": "100"}]
            }, {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [{"visibility": "off"}, {"lightness": "100"}]
            }, {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ffd4a5"}]
            }, {
                "featureType": "road.arterial",
                "elementType": "geometry.fill",
                "stylers": [{"color": "#ffe9d2"}]
            }, {
                "featureType": "road.local",
                "elementType": "all",
                "stylers": [{"visibility": "simplified"}]
            }, {
                "featureType": "road.local",
                "elementType": "geometry.fill",
                "stylers": [{"weight": "3.00"}]
            }, {
                "featureType": "road.local",
                "elementType": "geometry.stroke",
                "stylers": [{"weight": "0.30"}]
            }, {
                "featureType": "road.local",
                "elementType": "labels.text",
                "stylers": [{"visibility": "on"}]
            }, {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [{"color": "#747474"}, {"lightness": "36"}]
            }, {
                "featureType": "road.local",
                "elementType": "labels.text.stroke",
                "stylers": [{"color": "#e9e5dc"}, {"lightness": "30"}]
            }, {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [{"visibility": "on"}, {"lightness": "100"}]
            }, {"featureType": "water", "elementType": "all", "stylers": [{"color": "#d2e7f7"}]}]
        });

        // Steet View Button
        $('#streetView').click(function (e) {
            e.preventDefault();
            single_map.getStreetView().setOptions({visible: true, position: myLatlng});
            // $(this).css('display', 'none')
        });


        // Custom zoom buttons
        var zoomControlDiv = document.createElement('div');
        var zoomControl = new ZoomControl(zoomControlDiv, single_map);

        function ZoomControl(controlDiv, single_map) {

            zoomControlDiv.index = 1;
            single_map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(zoomControlDiv);

            controlDiv.style.padding = '5px';

            var controlWrapper = document.createElement('div');
            controlDiv.appendChild(controlWrapper);

            var zoomInButton = document.createElement('div');
            zoomInButton.className = "custom-zoom-in";
            controlWrapper.appendChild(zoomInButton);

            var zoomOutButton = document.createElement('div');
            zoomOutButton.className = "custom-zoom-out";
            controlWrapper.appendChild(zoomOutButton);

            google.maps.event.addDomListener(zoomInButton, 'click', function () {
                single_map.setZoom(single_map.getZoom() + 1);
            });

            google.maps.event.addDomListener(zoomOutButton, 'click', function () {
                single_map.setZoom(single_map.getZoom() - 1);
            });

        }


        // Marker
        var singleMapIco = "<i class='" + $('#singleListingMap').data('map-icon') + "'></i>";

        new CustomMarker(
            myLatlng,
            single_map,
            {
                marker_id: '1'
            },
            singleMapIco
        );


    }

    // Single Listing Map Init
    var single_map = document.getElementById('singleListingMap');
    if (typeof(single_map) != 'undefined' && single_map != null) {
        google.maps.event.addDomListener(window, 'load', singleListingMap);
    }

    // -------------- Single Listing Map / End -------------- //


    // Custom Map Marker
    // ----------------------------------------------- //

    function CustomMarker(latlng, map, args, markerIco) {
        this.latlng = latlng;
        this.args = args;
        this.markerIco = markerIco;
        this.setMap(map);
    }

    CustomMarker.prototype = new google.maps.OverlayView();

    CustomMarker.prototype.draw = function () {

        var self = this;

        var div = this.div;

        if (!div) {

            div = this.div = document.createElement('div');
            div.className = 'map-marker-container';

            div.innerHTML = '<div class="marker-container">' +
                '<div class="marker-card">' +
                '<div class="front face">' + self.markerIco + '</div>' +
                '<div class="back face">' + self.markerIco + '</div>' +
                '<div class="marker-arrow"></div>' +
                '</div>' +
                '</div>'


            // Clicked marker highlight
            google.maps.event.addDomListener(div, "click", function (event) {
                $('.map-marker-container').removeClass('clicked infoBox-opened');
                google.maps.event.trigger(self, "click");
                $(this).addClass('clicked infoBox-opened');
            });


            if (typeof(self.args.marker_id) !== 'undefined') {
                div.dataset.marker_id = self.args.marker_id;
            }

            var panes = this.getPanes();
            panes.overlayImage.appendChild(div);
        }

        var point = this.getProjection().fromLatLngToDivPixel(this.latlng);

        if (point) {
            div.style.left = (point.x) + 'px';
            div.style.top = (point.y) + 'px';
        }
    };

    CustomMarker.prototype.remove = function () {
        if (this.div) {
            this.div.parentNode.removeChild(this.div);
            this.div = null;
            $(this).removeClass('clicked');
        }
    };

    CustomMarker.prototype.getPosition = function () {
        return this.latlng;
    };

    // -------------- Custom Map Marker / End -------------- //


})(this.jQuery);
