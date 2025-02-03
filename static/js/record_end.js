document.addEventListener("DOMContentLoaded", function() {
    let path = JSON.parse(sessionStorage.getItem("path") || "[]");
    let watchID;
    let startTime = new Date(sessionStorage.getItem("startTime"));
    let totalDistance = 0;
    let caloriesBurned = 0;

    const showDistance = document.querySelector(".record__e_total_dist");
    const showCalories = document.querySelector(".record__e_total_cal");
    const showTime = document.querySelector(".record__e_total_time");

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

                        updateDisNCal();
                    },
                    (error) => console.error("실시간 좌표 수집 불가:", error),
                    { enableHighAccuracy: true, maximumAge: 1000, timeout: 5000}
                );
            },
            (error) => console.error("초기 좌표 수집 불가:", error),
            { enableHighAccuracy: true, timeout: 5000}
        );
    }

    function updateDisNCal() {
        totalDistance = calcDistance(path);
        caloriesBurned = totalDistance * 50; // 식 수정필요

        showDistance.textContent = `얼마걸음: ${totalDistance.toFixed(2)}km`;
        showCalories.textContent = `총 소비칼로리: ${caloriesBurned.toFixed(1)}kcal`;
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
            //start_time: startTime.toISOString(),
            start_time: sessionStorage.getItem("startTime"), // ✅ 프론트에서 KST로 변환한 값 사용
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