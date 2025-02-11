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

        let segments = []; // 전체 경로 저장
        let currentSegment = []; // gap 구분별 경로 저장(임시 저장소)

        // gap을 기준으로 경로 분리
        path.forEach((point) => {
            if(point === "gap") {
                if (currentSegment.length > 0) {
                    segments.push(currentSegment);
                    currentSegment = []; // 임시 저장소 초기화
                }
            } else {
                // gap이 나오기 전까지 임시 저장소 저장
                currentSegment.push({ lat: point.latitude, lng: point.longitude });
            }
        });

        // 1. 마지막 기록 강제 저장
        // 2. 기록동안 한번도 중지버튼을 사용하지 않은 경우
        if (segments.length === 0 && currentSegment.length > 0) {
            segments.push(currentSegment); 
        }

        segments.forEach(segment => {
            if (segment.length > 1) {
                let polyline = new google.maps.Polyline({
                    path: segment,
                    geodesic: true,
                    strokeColor: "#b82132",
                    strokeOpacity: 1.0,
                    strokeWeight: 5,
                });
                polyline.setMap(map);
            }
        });
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