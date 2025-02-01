document.addEventListener("DOMContentLoaded", function() {
    let path = JSON.parse(sessionStorage.getItem("path") || "[]");
    let watchID;

    console.log("저장된 경로 데이터: ", path);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                let initialPosition = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    timestamp: position.timestamp
                };

                path.push(initialPosition);
                sessionStorage.setItem("path", JSON.stringify(path));
                console.log("초기 좌표: ", initialPosition);

                watchID = navigator.geolocation.watchPosition(
                    (position) => {
                        let newPosition = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                            timestamp: position.timestamp
                        };
        
                        path.push(newPosition);
                        sessionStorage.setItem("path", JSON.stringify(path));
                        console.log("실시간 좌표: ", newPosition);
                    },
                    (error) => console.error("실시간 좌표 수집 불가:", error),
                    { enableHighAccuracy: true, maximumAge: 1000, timeout: 5000}
                );
            },
            (error) => console.error("초기 좌표 수집 불가:", error),
            { enableHighAccuracy: true, timeout: 5000}
        );
    }

    document.getElementById("stopBtn").addEventListener("click", function() {
        let endTime = new Date().toISOString(); // ISO 형식 저장
        let startTime = sessionStorage.getItem("startTime");

        navigator.geolocation.clearWatch(watchID);

        let totalDistance = calcDistance(path);
        let durationSec = (new Date(endTime) - new Date(startTime)) / 1000; // 초 단위로 변환
        let minutes = durationSec / 60; // 분 단위
        let pace = 0;
        if (totalDistance > 0) {
            pace = (minutes/totalDistance).toFixed(2);
        }
        let caloriesBurned = totalDistance * 50; // 식 수정해야 함

        function calcDistance(coords) {
            let totalDistance = 0;
            function haversine(lat1, lon1, lat2, lon2) {
                const R = 6371; // 지구 반지름
                const dLat = (lat2-lat1) * Math.PI / 180;
                const dLon = (lon2-lon1) * Math.PI / 180;
                const a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
                    + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180)
                    * Math.sin(dLon / 2) * Math.sin(dLon/2);
                const c = 2*Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                return R*c;
            }
            for (let i=1; i<coords.length; i++) {
                totalDistance += haversine(
                    coords[i-1].latitude, coords[i-1].longitude,
                    coords[i].latitude, coords[i].longitude
                );
            }
            return totalDistance;
        }

        // API에 보낼 데이터 구조
        let daily_record = {
            start_time: startTime,
            end_time: endTime,
            distance: totalDistance.toFixed(2),
            time: durationSec,
            pace: pace,
            calories: caloriesBurned.toFixed(1),
            path: path
        };

        // 서버로 데이터 전송
        fetch("/record/save_walk_record/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(daily_record)
        })
        .then(response => response.json())
        .then(data => {
            console.log("오늘걸음 기록 저장완료:", data);
            alert(`기록이 저장되었습니다.`);
        })
        .catch(error => console.error("기록 저장에 실패했습니다.", error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if(document.cookie && document.cookie != "") {
            let cookies = document.cookie.split(";");
            for (let i=0; i<cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name+"=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});