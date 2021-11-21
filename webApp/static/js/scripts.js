/*-------------------------------------------------- SCROLL/NAV --------------------------------------------------*/
	// affix the navbar after scroll below header
	$('#nav').affix({
	      offset: {
	        top: $('header').height()-$('#nav').height()
	      }
	});	
	// highlight the top nav as scrolling occurs
	$('body').scrollspy({ target: '#nav' });

	// smooth scrolling for scroll to top
	$('.scroll-top').click(function(){
	  $('body,html').animate({scrollTop:0},1000);
	});

	// smooth scrolling for nav sections 
	$('#nav .navbar-nav li>a').click(function(){
	  var link = $(this).attr('href');
	  var posi = $(link).offset().top;
	  $('body,html').animate({scrollTop:posi},700);
	});

	// tooltips
	$('#province').tooltip();
	$('#road').tooltip();
	$('#pk').tooltip();
	$('#activate').tooltip();
	$('#deactivate').tooltip();
	$('#deact1').tooltip();
/*-------------------------------------------------- Chart --------------------------------------------------*/
    var chart;
    var ChartData = [];
    var restTimeCompleted = false;

	    AmCharts.ready(function () {

	        // SERIAL CHART
	        chart = new AmCharts.AmSerialChart();
	        chart.pathToImages = "static/images/amcharts/";
	        chart.dataProvider = ChartData;
	        chart.categoryField = "date";
	        chart.autoMargins = "true";


	        // AXES
	        // Category
	        var categoryAxis = chart.categoryAxis;
	        categoryAxis.parseDates = true; // in order char to understand dates, we should set parseDates to true
	        categoryAxis.minPeriod = "mm"; // as we have data with minute interval, we have to set "mm" here.       
	        categoryAxis.gridAlpha = 0.0;
	        categoryAxis.axisColor = "#DADADA";

	        // Value
	        var valueAxis = new AmCharts.ValueAxis();
	        valueAxis.gridAlpha = 0.0;
	        valueAxis.title = "IMT (índice medio de tráfico)";
	        valueAxis.axisColor = "#DADADA";
	        chart.addValueAxis(valueAxis);

	        // GRAPH
	        var graph = new AmCharts.AmGraph();
	        graph.type = "smoothedLine"; // try to change it to "column"
	        graph.title = "IMT (índice medio de trádfico)";
	        graph.valueField = "imt";
	        graph.lineThickness = 1;
	        graph.lineAlpha = 1;
	        graph.lineColor = "#37474F";
	        graph.fillAlphas = 0.3; // setting fillAlphas to > 0 value makes it area graph
	        graph.bullet = "round";
	        graph.bulletSize = 10;
	        graph.bulletColor = "#FFFFFF";
	        graph.bulletBorderColor = "#1F282D";
	        graph.bulletBorderThickness = 2;
	        graph.bulletBorderAlpha = 1;
	        graph.balloonText = "<div style='margin-top:20px;margin-bottom:20px;text-shadow: 2px 2px rgba(0, 0, 0, 0.1); font-weight:200;font-size:30px; color:#000000'>[[value]]</div>"
	        chart.addGraph(graph);

	        // CURSOR
	  		var chartCursor = new AmCharts.ChartCursor();
	  		chartCursor.cursorAlpha = 0.2;
	  		chartCursor.zoomable = false;
	  		chartCursor.cursorColor = "#1F282D";
	  		chartCursor.categoryBalloonColor = "#55646D";
	  		chartCursor.fullWidth = true;
	  		chartCursor.categoryBalloonDateFormat = "JJ:NN, DD MMMM";
	  		chartCursor.balloonPointerOrientation = "vertical";
	  		chart.addChartCursor(chartCursor);

	        // BALLOON
	        var balloon = chart.balloon;
	        balloon.borderAlpha = 0;
	        balloon.fillAlpha = 0;
	        balloon.shadowAlpha = 0;
	        balloon.offsetX = 10;
	        balloon.offsetY = -50;

	        // SCROLLBAR
	        var chartScrollbar = new AmCharts.ChartScrollbar();

	        chart.addChartScrollbar(chartScrollbar);
	        chart.amExport = {};

	        // WRITE
	        chart.write("chartdiv");
	    });

	function loadTimeoutBar(time_) {
	     $("#progressTimer").progressTimer({
		    timeLimit: time_,
		    warningThreshold: 10,
		    baseStyle: 'progress-bar-custom',
		    warningStyle: 'progress-bar-custom',
		    completeStyle: 'progress-bar-success',
		    onFinish: function() {
			        restTimeCompleted = true;
			    }
		});
	}

    // update loaded chart
    function updateChart(codEle_) {
    	var sse = new EventSource("/updateChart");
    	sse.onmessage = function(event) {
    		var imt = event.data;
    		obj = JSON.parse(imt);

    		chart.dataProvider.push({
	              date: new Date(obj.elements[0]["timestamp"]),
	              imt: obj.elements[0]["imt"]
	            });
    		chart.validateData();
		  	$('#dataImage_ori img').attr('src', 'static/tmp/'+codEle_+'_ori.jpg?nocache=' + (new Date()).getTime());
			//$('#dataImage_proc img').toggleClass('hidden');
	  		//$('#dataImage_proc img').attr('src', 'static/tmp/'+codEle_+'_proc.jpg?nocache=' + (new Date()).getTime());
		}
    }
 

    // reload data contents on chart
    function initChartData(codEle_) {
    	chart.dataProvider = [];
    	chart.validateData();
    	$.getJSON($SCRIPT_ROOT + '/initChart',{
				codEle: codEle_
			}, function(data) {
				for(key in data.elements) {
		            chart.dataProvider.push({
		              date: new Date(data.elements[key]["timestamp"]),
		              imt: data.elements[key]["imt"]
		            });
		    	}
		    	chart.validateData();
		    	updateChart(codEle_);
			  	$('#dataImage_ori img').attr('src', 'static/tmp/'+codEle_+'_ori.jpg?nocache=' + (new Date()).getTime());
				//$('#dataImage_proc img').toggleClass('hidden');
		  		//$('#dataImage_proc img').attr('src', 'static/tmp/'+codEle_+'_proc.jpg?nocache=' + (new Date()).getTime());

			  	/*
			  	if (data.elements[data.elements]["proc_img"] == "saved") {
			  		$('#dataImage_proc img').attr('src', 'static/tmp/'+codEle_+'_proc.jpg?nocache=' + (new Date()).getTime());
			  	}*/

		    	//var restTime = Math.abs((5 - (new Date().getMinutes() - chart.dataProvider[chart.dataProvider.length-2]["date"].getMinutes()))*60);
				//loadTimeoutBar(restTime);

		});

    	chart.validateData();
    	updateChart(codEle_);
	  	$('#dataImage_ori img').attr('src', 'static/tmp/'+codEle_+'_ori.jpg?nocache=' + (new Date()).getTime());
    }



/*-------------------------------------------------- MAPS --------------------------------------------------*/
var map;
var myCenter;
var markers = [];
var cameras = [];
var fullscreenActive = false;

	  // FULLSCREEN FUNCTS
	    function FullScreen() {
	        var element = $("#googleMap")[0];
	        

			if (fullscreenActive == true)
			{
				if(document.exitFullscreen) {
				    document.exitFullscreen();
				} else if(document.mozCancelFullScreen) {
				    document.mozCancelFullScreen();
				} else if(document.webkitExitFullscreen) {
				    document.webkitExitFullscreen();
				}
				fullscreenActive = false;
			} else {
		        if (element.requestFullScreen) {
		            element.requestFullScreen();
		        } else if (element.webkitRequestFullScreen) {
		            element.webkitRequestFullScreen();
		        }else if (element.mozRequestFullScreen) {
		            element.mozRequestFullScreen();
		        } else if(element.msRequestFullscreen) {
				    element.msRequestFullscreen();
				}		
				fullscreenActive = true;			
			}
	    }

	    function exitFullscreen() {
		  if(document.exitFullscreen) {
		    document.exitFullscreen();
		  } else if(document.mozCancelFullScreen) {
		    document.mozCancelFullScreen();
		  } else if(document.webkitExitFullscreen) {
		    document.webkitExitFullscreen();
		  }
		}

	    function FullScreenControl(controlDiv, map) {

	      // Set CSS for the control border
	      var controlUI = document.createElement('div');
	      controlUI.style.backgroundColor = '#fff';
	      controlUI.style.border = '1px solid #fff';
	      controlUI.style.borderRadius = '3px';
	      controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
	      controlUI.style.cursor = 'pointer';
	      controlUI.style.marginBottom = '25px';
	      controlUI.style.textAlign = 'center';
	      controlUI.title = 'Pantalla completa';
	      controlDiv.appendChild(controlUI);

	      // Set CSS for the control interior
	      var controlText = document.createElement('div');
	      controlText.style.color = 'rgb(92,92,92)';
	      controlText.style.fontSize = '15px';
	      controlText.style.lineHeight = '38px';
	      controlText.style.paddingLeft = '5px';
	      controlText.style.paddingRight = '5px';
	      controlText.innerHTML = '<i class="glyphicon glyphicon-fullscreen"></i>';
	      controlUI.appendChild(controlText);

	      google.maps.event.addDomListener(controlUI, 'click', function() {
	        FullScreen();
	      });

	    }

	    // SHOW MARKER DATA
	    function showData(codEle) {

	      $('#dataShown').removeClass("hidden");
  		  $('#dataImage_ori img').attr('src', 'static/tmp/'+codEle+'_ori.jpg?nocache=' + (new Date()).getTime());
		  initChartData(codEle);
		  //loadTimeoutBar();
	      $('body,html').animate({scrollTop: $("#dataImage_ori").offset().top}, 700);
	    }


	    // MARKERS FUNCTS
	    function setMarkers() {
	      var image = '../static/images/marker.png';
	      
	      for (var i = 0; i < cameras.length; i++) {
	          var cam = cameras[i];
	          var myLatLng = new google.maps.LatLng(cam[1], cam[2]);
	          // only add animation if not all markers are requested
	          if (cameras.length < 30) {
	            var marker = new google.maps.Marker({
	                icon: image,
	                position: myLatLng,
	                map: map,
	                title: cam[0]
	            });
	          }
	          else {
	            var marker = new google.maps.Marker({
	                icon: image,
	                position: myLatLng,
	                map: map,
	                title: cam[0],
	                id: cam[0]
	            });
	          }

	          // Push marker to markers array
	          markers.push(marker);

	          // add event listener on click
	          (function(codEle, markr){
	           google.maps.event.addListener(marker,'click',function() {
	              map.setZoom(10);                                      // zoom on map with marker on center
	              map.setCenter(markr.getPosition());
              	  showData(codEle);
              	  $('#deact1').attr('value', codEle);
			   });
	          })(cam[0], marker);
	      }
	    }

	  	// Reload markers on map
	    function reloadMarkers() {
	      // update markers from activated cameras
	      var key;
	      cameras = [];
	      var data = $.parseJSON($.ajax({
	          type: "GET",
	          url: $SCRIPT_ROOT + '/updateMaps',
	          crossDomain: true,
	          cache: false,
	          data: "json",
	          async: false
	         }).responseText);
			for(key in data.elements) {
		        cameras.push([data.elements[key]["codEle"],
		                    data.elements[key]["lat"],
		                    data.elements[key]["lng"]]
		                    );
		    }
	      
	      // Loop through markers and set map to null for each
	      for (var i=0; i<markers.length; i++) {
	          markers[i].setMap(null);
	      }
	      // Reset the markers array
	      markers = [];
	      // Call set markers to re-add markers
	      setMarkers();
	  }


	// MAP INITIALIZE
	  function initialize() {
	     var mapOptions = {
	       center: new google.maps.LatLng(40.5252821,-3.8160297),
	       zoom: 6,
	       mapTypeControl: true,
	       mapTypeControlOptions: {
	         style: google.maps.MapTypeControlStyle.ROADMAP,
	         mapTypeIds: [
	           google.maps.MapTypeId.HYBRID,
	           google.maps.MapTypeId.ROADMAP
	         ]
	       },
	       zoomControl: true,
	       zoomControlOptions: {
	         style: google.maps.ZoomControlStyle.SMALL
	       }
	       };
	      map = new google.maps.Map(document.getElementById("googleMap"),mapOptions);
	      
	      reloadMarkers();

	      var FullScreenControlDiv = document.createElement('div');
	      var fullscreenControl = new FullScreenControl(FullScreenControlDiv, map);
	      FullScreenControlDiv.index = 10;
	      map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(FullScreenControlDiv);
	  }

	  google.maps.event.addDomListener(window, 'load', initialize);

/*-------------------------------------------------- LOCATOR MANAGER --------------------------------------------------*/

// load province options on load
$(document).ready(function() {
	$.getJSON($SCRIPT_ROOT + '/updateProvince', function(data) {
			for(key in data.elements) {
				$("#province").append($('<option></option>').attr("value",data.elements[key]["province"]).text(data.elements[key]["province"]));
			}
	});
});

// Onchange province selector to get road, way and pk datalist with ajax
$("#province").change(function(){
	document.getElementById("road").innerHTML = '<option value="default">Elija una opción...</option>';
	document.getElementById("pk").innerHTML = '<option value="default">Elija una opción...</option>';

	if ($(this).val() != "default") {
		$.getJSON($SCRIPT_ROOT + '/updateRoad',{
				province: $(this).val()
			}, function(data) {
				for(key in data.elements) {
					$("#road").append($('<option></option>').attr("value",data.elements[key]["road"]).text(data.elements[key]["road"]));
				}
            document.getElementById("pk").innerHTML = '<option value="default">Elija una opción...</option>'; 
		});
	}
	
});
$("#road").change(function(){
	document.getElementById("pk").innerHTML = '<option value="default">Elija una opción...</option>';

	if ($(this).val() != "default") {
		$.getJSON($SCRIPT_ROOT + '/updatePK',{
				province: $("#province").val(),
				road: $(this).val()
			}, function(data) {
				for(key in data.elements) {
					$("#pk").append($('<option></option>').attr("value",data.elements[key]["pk"]).text(data.elements[key]["pk"]));
				}
		});
	}
	
});

// make function depending selected option in form
function updateCamStats(stat) {
	//send option to application
    $.ajax({
      type: "GET",
      url: $SCRIPT_ROOT + "/updateCam",
      crossDomain: true,
      cache: false,
      data: "json",
      async: false,
      data: { option: stat,
            province: $("#province").val(), 
            road: $("#road").val(), 
            pk: $("#pk").val() 
            },
      success: function(data) {
      }
    });    
}
// make function depending selected option in form
function deactivateOneCamStats() {
	//send option to application
    $.ajax({
      type: "GET",
      url: $SCRIPT_ROOT + "/deactivateOneCam",
      crossDomain: true,
      cache: false,
      data: "json",
      async: false,
      data: { 
            codEle: $("#deact1").val() 
            },
      success: function(data) {
      }
    });    
}
$(function() {
	$("#activate").click(function() {
		if (document.getElementById("province").value == 'default' && !confirm('Todas las cámaras serán ACTIVADAS.'+'\n'+' ¿Esta seguro de realizar esta acción?')) {
	            return;
	    }
	    updateCamStats("activate");
	    // load cameras on map
		reloadMarkers();
		map.setZoom(6);                                      // zoom on map with marker on center
		map.setCenter(new google.maps.LatLng(40.5252821,-3.8160297));
	});
	$("#deactivate").click(function() {
		if (document.getElementById("province").value == 'default' && !confirm('Todas las cámaras serán DESACTIVADAS.'+'\n'+' ¿Esta seguro de realizar esta acción?')) {
	            return;
	    }
	    updateCamStats("deactivate");
	    // load cameras on map
		reloadMarkers();
        $('body,html').animate({scrollTop: $("#googleMap").offset().top}, 700);
        $('#dataShown').addClass("hidden");
		map.setZoom(6);                                      // zoom on map with marker on center
		map.setCenter(new google.maps.LatLng(40.5252821,-3.8160297));
	});
	$("#deact1").click(function() {
	    deactivateOneCamStats();
	    // load cameras on map
		reloadMarkers();
        $('body,html').animate({scrollTop: $("#googleMap").offset().top}, 700);
        $('#dataShown').addClass("hidden");
		map.setZoom(6);                                      // zoom on map with marker on center
		map.setCenter(new google.maps.LatLng(40.5252821,-3.8160297));
	});
});
