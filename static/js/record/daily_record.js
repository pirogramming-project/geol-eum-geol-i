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

    // Google Maps UI Custom
    const customMapStyle = [
        {
            elementType: "geometry",
            stylers: [{ color: "#1F1F1F" }] // 배경: 블랙
        },
        {
            elementType: "labels.text.fill",
            stylers: [{ color: "#D4AF37" }] // 텍스트: 연한 골드
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [{ color: "#2B3A42" }] // 물: 네이비
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [{ color: "#C8A961" }] // 기본 도로: 골드
        },
        {
            featureType: "road.arterial",
            elementType: "geometry",
            stylers: [{ color: "#E0C68D" }] // 주요 도로: 밝은 골드
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{ color: "#A17C48" }] // 고속도로: 어두운 골드
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry",
            stylers: [{ color: "#D4AF37" }] // 주요 고속도로: 짙은 골드
        },
        {
            featureType: "transit",
            stylers: [{ visibility: "off" }] // 대중교통 요소 숨기기
        },
        {
            featureType: "poi",
            stylers: [{ visibility: "simplified"}, {color: "#E0C68D" }] // POI(주요시설): 옐로우
        }
    ];

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
                styles: customMapStyle, // 커스텀한 UI 적용
            });
        } else {
            // 지도 존재 시, 경로에 맞춰 세팅
            map.setCenter({ lat: path[0].latitude, lng: path[0].longitude });
            map.setOptions({ styles: customMapStyle });
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
                    // gap 이전의 경로 저장
                    segments.push(currentSegment);
                    currentSegment = []; // 임시 저장소 초기화
                }
            } else {
                // gap이 나오기 전까지 임시 저장소 저장
                currentSegment.push({ lat: point.latitude, lng: point.longitude });
            }
        });

        // 모두 currentSegment에 저장한(일시정지 버튼 사용하지 않은) 경우
        if (segments.length === 0) {
            segments.push(currentSegment); 
        }
        // 마지막 gap 이후 GPS 좌표들이 남은(일지정지 후 수집재개하지 않고 기록 종료) 경우
        if (currentSegment.length > 0) {
            segments.push(currentSegment); 
        }

        segments.forEach(segment => {
            // 일시정지 버튼 전까지의 각각의 경로를 각각의 폴리라인으로 나타내기
            if (segment.length > 1) {
                let polyline = new google.maps.Polyline({
                    path: segment,
                    geodesic: true,
                    strokeColor: "#b82132",
                    strokeOpacity: 0.9,
                    strokeWeight: 6,
                    icons: [
                        {
                            icon: {
                                path: google.maps.SymbolPath.CIRCLE,
                                scale: 5,
                                strokeColor: "#d2665a",
                                strokeOpacity: 0.8
                            },
                            offset: "100%"
                        }
                    ]
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

// 이미지 파일 선택 후 파일 이름 표시
document.getElementById("file-upload").addEventListener("change", function(event) {
    const fileName = event.target.files[0] ? event.target.files[0].name : "선택된 파일 없음";
    document.getElementById("file-name").textContent = fileName;
});