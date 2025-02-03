document.addEventListener("DOMContentLoaded", function() {
    const mapButtons = document.querySelectorAll(".daily__route_map");

    console.log("Django의 path 데이터:", djangoPathData);
    let paths = djangoPathData;
    sessionStorage.setItem("path", JSON.stringify(paths));

    console.log("sessionStorage 업데이트: ", paths);

    if(mapButtons.length > 0) {
        mapButtons.forEach((mapBtn, index) => {
            mapBtn.addEventListener("click", function() {
                let recordID = mapBtn.getAttribute("data-record-id");
                let path = paths[index];

                if (!path) {
                    alert("저장된 경로 데이터 없음.");
                    return;
                }
    
                let mapContainerID = `map-${recordID}`;
                let map_exist = document.getElementById("map");
                if (map_exist) {
                    map_exist.remove();
                }
                let mapContainer = document.createElement("div");
                mapContainer.id = mapContainerID;
                mapContainer.style.width = "100%";
                mapContainer.style.height = "500px";
                document.body.appendChild(mapContainer);
    
                if (typeof google !== "undefined" && google.maps) {
                    console.log(`initMap() 호출 직전 ${recordID} path 값:`, path);
                    setTimeout(() => window.initMapForRecord(path, mapContainerID), 100);
                }
            });
        });
    }
});

window.initMap = function() {
    console.log("기본 initMap 실행");
};

window.initMapForRecord = function(path, mapContainerID) {
    console.log(`initMap()에서 받은 ${mapContainerID} path: `, path);

    let map = new google.maps.Map(document.getElementById(mapContainerID), {
        center: {lat: path[0].latitude, lng: path[0].longitude},
        zoom: 15,
    });

    let routePath = new google.maps.Polyline({
        path: path.map((point) => ({ lat:point.latitude, lng: point.longitude })),
        geodesic: true,
        strokeColor: "#ffa79d",
        strokeOpacity: 1.0,
        strokeWeight: 5,
    });

    routePath.setMap(map);
}