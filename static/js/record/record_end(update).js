document.addEventListener("DOMContentLoaded", function () {
    let path = [];
    let watchID;
    let totalDistance = 0;
    let caloriesBurned = 0;
    let weight = 75;
    let minDistance = 3; // ✅ 최소 3m 이상 이동 시에만 기록

    const showDistance = document.querySelector(".record__e_total_dist");
    const showCalories = document.querySelector(".record__e_total_cal");
    const showTime = document.querySelector(".record__e_total_time");

    let now = new Date();
    now.setHours(now.getHours() + 9);
    let startTime = now.toISOString().slice(0, 19);

    console.log("📌 저장된 경로 데이터: ", path);

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
                console.log("📍 초기 좌표 추가됨:", initialPosition);

                watchID = navigator.geolocation.watchPosition(
                    (position) => {
                        let newPosition = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                            timestamp: position.timestamp
                        };

                        if (path.length > 0) {
                            let lastPosition = path[path.length - 1];

                            // ✅ 이동 거리 계산 (단위: km)
                            let distance = haversine(
                                lastPosition.latitude, lastPosition.longitude,
                                newPosition.latitude, newPosition.longitude
                            );

                            // ✅ 동일한 시간 데이터는 중복 저장 방지
                            if (newPosition.timestamp === lastPosition.timestamp) {
                                console.log("⚠️ 동일한 시간 데이터 → 중복 저장 방지");
                                return;
                            }

                            // ✅ GPS 흔들림 방지 (위도·경도 변화량이 너무 작으면 무시)
                            if (
                                Math.abs(newPosition.latitude - lastPosition.latitude) < 0.00001 &&
                                Math.abs(newPosition.longitude - lastPosition.longitude) < 0.00001
                            ) {
                                console.log("⚠️ 너무 작은 변화량 → GPS 오차 가능성 있음, 무시함");
                                return;
                            }

                            // ✅ 3m 이상 이동 시에만 기록
                            if (distance >= minDistance / 1000) {
                                path.push(newPosition);
                                sessionStorage.setItem("path", JSON.stringify(path));
                                console.log(`📍 실시간 좌표 추가됨 (${(distance * 1000).toFixed(2)}m 이동):`, newPosition);
                                updateDisNCal();
                            } else {
                                console.log(`⚠️ 이동 거리 너무 작음 (${(distance * 1000).toFixed(2)}m) → 무시됨`);
                            }

                        } else {
                            // ✅ 첫 번째 위치는 무조건 추가
                            path.push(newPosition);
                            sessionStorage.setItem("path", JSON.stringify(path));
                            console.log("📍 초기 좌표 추가됨:", newPosition);
                        }
                    },
                    (error) => console.error("🚨 실시간 좌표 수집 불가:", error),
                    { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
                );
            },
            (error) => console.error("🚨 초기 좌표 수집 불가:", error),
            { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
        );
    }

    function haversine(lat1, lon1, lat2, lon2) {
        const R = 6371; // 지구 반지름 (km)
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c; // 거리 (km)
    }

    function updateDisNCal() {
        totalDistance = calcDistance(path);
        let durationSec = Math.floor((new Date() - startTime) / 1000);
        let minutes = durationSec / 60;
        caloriesBurned = calcCalories(totalDistance, minutes, weight);

        showDistance.textContent = `얼마걸음: ${totalDistance.toFixed(2)}km`;
        showCalories.textContent = `총 소비칼로리: ${caloriesBurned}kcal`;
    }

    function updateTime() {
        let now = new Date();
        let durationSec = Math.floor((now-startTime)/1000); // 초 단위변환
        let hours = Math.floor(durationSec/3600);
        let min = Math.floor((durationSec % 3600)/60);
        let sec = durationSec % 60;

        showTime.textContent = `${hours.toString().padStart(2, "0")}:${min.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
    }

    function calcDistance(coords) {
        let totalDistance = 0;
        for (let i = 1; i < coords.length; i++) {
            totalDistance += haversine(
                coords[i - 1].latitude, coords[i - 1].longitude,
                coords[i].latitude, coords[i].longitude
            );
        }
        return totalDistance;
    }

    function calcCalories(dist, time, weight) {
        let speed = dist / (time/60); // km/h 계산하기 위함
        let METs;

        if (speed < 5.5) {
            METs = 3.8;
        } else if (speed < 8.0) {
            METs = 4.3;
        } else {
            METs = 7.0;
        }
        return parseInt(METs * weight * (time/60)); // 정수형으로 변환
    }

    let timeUpdate = setInterval(updateTime, 1000);

    document.getElementById("stopBtn").addEventListener("click", function() {
        let now = new Date();
        now.setHours(now.getHours() + 9); // ✅ UTC+9(KST) 변환
        let endTime = now.toISOString().slice(0, 19); // YYYY-MM-DDTHH:MM:SS 형식

        navigator.geolocation.clearWatch(watchID);
        clearInterval(timeUpdate);

        let durationSec = Math.floor((new Date(endTime) - startTime) / 1000); // 초 단위로 변환
        let minutes = durationSec / 60; // 분 단위
        let pace = 0.00;
        if (totalDistance > 0) {
            pace = (minutes/totalDistance).toFixed(2);
        }

        let today = new Date();
        let year = today.getFullYear();
        let month = String(today.getMonth()+1).padStart(2, "0"); // getMonth(0~11) 이므로 범위 보정
        let day = String(today.getDate()).padStart(2, "0");
        let formattedDate = `${year}-${month}-${day}`;

        // API에 보낼 데이터 구조
        let daily_record = {
            start_time: startTime, // ✅ 프론트에서 KST로 변환한 값 사용
            end_time: endTime, // ✅ KST로 변환된 값 전송
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

            sessionStorage.clear();

            window.location.href = `/record/history/${formattedDate}/`;
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
