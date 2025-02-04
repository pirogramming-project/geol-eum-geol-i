document.addEventListener("DOMContentLoaded", function() {
    const mapButton = document.querySelector(".daily__route_map");
    const modal = document.getElementById("mapModal");
    const closeModalBtn = document.querySelector(".close");
    const mapContainer = document.getElementById("map");

    const paginationLinks = document.querySelectorAll(".pagination a");
    paginationLinks.forEach(link => {
        link.addEventListener("click", function() {
            window.scrollTo({ top:0, behavior: "smooth" });
        });
    });

    let map = null; // 지도 객체
    let routePath = null; // 경로 업데이트를 위한 변수

    closeModalBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Google Maps API 로드 실행
    function loadGoogleMaps(callback) {
        callback();
    }

    sessionStorage.setItem("path", JSON.stringify(djangoPathData));

    // 지도 초기화 및 특정 기록의 경로 표시
    function showMap() {
        let path = JSON.parse(sessionStorage.getItem("path"));
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
            strokeColor: "#7200FF",
            strokeOpacity: 1.0,
            strokeWeight: 5,
        });
        routePath.setMap(map);
    }

    if(mapButton) {
        mapButton.addEventListener("click", function() {
            loadGoogleMaps(() => showMap());
        });
    }
});

// 파일 선택 후 파일 이름 표시
document.getElementById("file-upload").addEventListener("change", function(event) {
    const fileName = event.target.files[0] ? event.target.files[0].name : "선택된 파일 없음";
    document.getElementById("file-name").textContent = fileName;
});