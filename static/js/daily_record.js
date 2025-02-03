document.addEventListener("DOMContentLoaded", function() {
    const mapButtons = document.querySelectorAll(".daily__route_map");
    const modal = document.getElementById("mapModal");
    const closeModalBtn = document.querySelector(".close");
    const mapContainer = document.getElementById("map");
    let map = null; // 지도 객체
    let routePath = null; // 경로 업데이트를 위한 변수

    closeModalBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Google Maps API 로드 실행
    function loadGoogleMaps(callback) {
        callback();
    }

    // 지도 초기화 및 특정 기록의 경로 표시
    function showMap(path) {
        console.log("경로: ", path);

        modal.style.display = "flex";

        if (!map) {
            // 지도 없으면 새롭게 생성
            map = new google.maps.Map(mapContainer, {
                center: { lat: path[0].latitude, lng: path[0].longitude },
                zoom: 15,
            });
        } else {
            // 지도 존재 시, 경로에 맞춰 세팅
            map.setCenter({ lat: path[0].latitude, lng: path[0].longitude });
        }

        if (routePath) {
            // 기존 경로 지우기
            routePath.setMap(null);
        }
        routePath = new google.maps.Polyline({
            path: path.map((point) => ({ lat: point.latitude, lng: point.longitude })),
            geodesic: true,
            strokeColor: "#ffa79d",
            strokeOpacity: 1.0,
            strokeWeight: 5,
        });
        routePath.setMap(map);
    }

    if(mapButtons.length > 0) {
        mapButtons.forEach((mapBtn, index) => {
            mapBtn.addEventListener("click", function() {
                let paths = djangoPathData;
                sessionStorage.setItem("path", JSON.stringify(paths));
                let path = paths[index];

                if (!path) {
                    alert("저장된 경로 데이터 없음.");
                    return;
                }

                loadGoogleMaps(() => showMap(path));
            });
        });
    }
});