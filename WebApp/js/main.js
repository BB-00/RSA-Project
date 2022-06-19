const obuIcon = L.icon({
    iconUrl: 'img/blue-circle.png',
    iconSize: [10, 10],
    iconAnchor: [5, 5]
});
const rsuIcon = L.icon({
    iconUrl: 'img/yellow-circle.png',
    iconSize: [10, 10],
    iconAnchor: [5, 5]
});
const truckIcon = L.icon({
    iconUrl: 'img/green-circle.png',
    iconSize: [10, 10],
    iconAnchor: [5, 5]
});

var map = L.map('mapid').setView([40.64,-8.65], 15); // Start centered in Aveiro
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmljYXJkbzAzYyIsImEiOiJjanZhNHF4N2QwdXZxM3lucmJtcTVvZDdzIn0.37cwnhfRcjk3cVN0HQugsQ',
{attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
maxZoom: 22,
tileSize: 512,
zoomOffset: -1,
id: 'mapbox/dark-v10',
accessToken: 'pk.eyJ1IjoicmljYXJkbzAzYyIsImEiOiJjanZhNHF4N2QwdXZxM3lucmJtcTVvZDdzIn0.37cwnhfRcjk3cVN0HQugsQ'
}).addTo(map);

var currentmarkersRSU = L.layerGroup().addTo(map);
var currentmarkersOBU = L.layerGroup().addTo(map);
var graph             = L.layerGroup().addTo(map);
var positions = {};     // {id:[lat,lon],...} - Current position of each node
var progressIDs = [];   // List with progress bar's IDs
var doneList = {};      // nodes that have finished the transfer
var startedList = {};   // nodes that have started the transfer
var currentTS = 0;

// Handles START button click - id="btn_start"
// Calls /start and blocks.
function clickStart(){
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/start", true);
    xmlHttp.send( null );
    document.getElementById("btn_start").disabled = true;
}

// Handles STOP button click - id="btn_stop"
function clickStop(){
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/stop", true);
    xmlHttp.send( null );
    document.getElementById("btn_start").disabled = false;
    window.location.reload(false);
}

// Helper function to change a 'domID' text field to 'text'.
function changeText(domID,text){
    // Compares previous value with the new one to prevent needless refreshes.
    if (document.getElementById(domID).innerText != text){
        document.getElementById(domID).innerText = text;
    }
}

// Make required changes in the map, according to the new data.
function updateMap(data){
    updateMarkers(data);
    //updateGraph(data);
}

// Updates RSU and OBU markers for the new positions.
function updateMarkers(data){
    // Clear and update markers
    currentmarkersOBU.clearLayers();
    currentmarkersRSU.clearLayers();
    for(i = 0; i < data.length; i++){
        if('timestamp' in data[i]){
            continue;
        }
        var node = data[i];
        var marker = null;
        if (node['rsu'] == 1){
            marker = L.marker([node['lat'],node['lon']], {icon:rsuIcon});
            marker.bindPopup("ID: "+node['id']+", RSU").openPopup();
            marker.addTo(currentmarkersRSU);
        }else{
            marker = L.marker([node['lat'],node['lon']], {icon:obuIcon});
            marker.bindPopup("ID: "+node['id']).openPopup();
            marker.addTo(currentmarkersOBU);
        }
        // Update 'positions' structure
        positions[node['id']] = new L.LatLng(node['lat'], node['lon']);
    }
}

// Pulls status information from the sim_manager and calls parseData() when ready.
function requestData(){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200)
            parseData(xmlHttp.responseText);
    }
    xmlHttp.open( "GET", "/status", true);
    xmlHttp.send( null );
}

// Main function called for every received request (data).
function parseData(data){
    try{
        data = JSON.parse(data);
    }catch(err){
        changeText("sim_status",data);
        return;
    }
    changeText("sim_status","Simulation running.");
    updateMap(data);
    updateProgress(data);
}

// setInterval(requestData, 5000);
