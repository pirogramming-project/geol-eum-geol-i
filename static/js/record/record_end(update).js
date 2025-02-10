document.addEventListener("DOMContentLoaded", function () {
    localStorage.removeItem('gpsData'); // 새로운 걸음기록 시작마다 GPS 데이터 초기화
    let path = [];
    let watchID;
    let totalDistance = 0;
    let caloriesBurned = 0;
    let weight = 75;
    let minDistance = 3; // 최소 3m 이상 이동 시에만 기록
    let isPaused = false; // 기록 수집 상태 확인용
    let pauseStartTime = null; // bottleBtn 누른 시간
    let totalPausedTime = 0; // 총 기록 수집 중단 시간

    const showDistance = document.querySelector(".record__e_total_dist");
    const showCalories = document.querySelector(".record__e_total_cal");
    const showTime = document.querySelector(".record__e_total_time");
    const showStatus = document.querySelector(".record__e_status");

    let startTime = new Date();
    startTime.setHours(startTime.getHours() + 9);

    console.log("📌 저장된 경로 데이터: ", path);

    function getUserGPS() {
        if (navigator.geolocation) {
            watchID = navigator.geolocation.watchPosition(
                (position) => {
                    if (isPaused) {
                        return;
                    }

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
                            console.log(`📍 실시간 좌표 추가됨 (${(distance * 1000).toFixed(2)}m 이동):`, newPosition);
                            updateDisNCal();

                            // Background Sync 등록 -> 백그라운드 모드(모바일 화면 종료 or 오프라인) GPS 유지
                            registerBackgroundSync(path);
                        } else {
                            console.log(`⚠️ 이동 거리 너무 작음 (${(distance * 1000).toFixed(2)}m) → 무시됨`);
                        }
    
                    } else {
                        path.push(newPosition);
                        console.log("📍 초기 좌표 추가됨:", newPosition);
                    }
                },
                (error) => console.error("🚨 실시간 좌표 수집 불가:", error),
                { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
            );
        }
    }

    function stopUserGPS() {
        if (watchID) {
            navigator.geolocation.clearWatch(watchID);
            watchID = null;
        }
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

        // 현재 시간을 KST로 변환
        let currentTime = new Date();
        currentTime.setHours(currentTime.getHours() + 9); // UTC → KST 변환

        // KST 기준으로 경과 시간 계산
        let durationSec = Math.floor((currentTime - startTime) / 1000) - totalPausedTime;

        let minutes = durationSec / 60;

        // 초기에는 칼로리 계산을 하지 않음
        if (minutes < 0.5) {
            console.log("⚠️ 30초 미만 → 칼로리 계산 제외");
            showDistance.textContent = ` 얼마걸음: ${totalDistance.toFixed(2)}km`;
            showCalories.textContent = `총 소비칼로리: 0kcal`;
            return;
        }

        caloriesBurned = calcCalories(totalDistance, minutes, weight);

        // UI 업데이트 최적화: 이전 값과 비교하여 DOM 업데이트 최소화
        const newDistanceText = ` 얼마걸음: ${totalDistance.toFixed(2)}km`;
        const newCaloriesText = `총 소비칼로리: ${caloriesBurned}kcal`;

        if (totalDistance < 0.01) {
            console.log("⚠️ 30초 미만 & 거리 부족 → UI 초기화");
            if (showDistance.textContent !== `얼마걸음: 0.00km`) {
                showDistance.textContent = `얼마걸음: 0.00km`;
            }
            if (showCalories.textContent !== `총 소비칼로리: 0kcal`) {
                showCalories.textContent = `총 소비칼로리: 0kcal`;
            }
            return;
        }

        if (showDistance.textContent !== newDistanceText) {
            showDistance.textContent = newDistanceText;
        }
        if (showCalories.textContent !== newCaloriesText) {
            showCalories.textContent = newCaloriesText;
        }
    }

    function updateTime() {
        if (isPaused) {
            return;
        } // 기록수집 중단상태면 시간 업데이트 중지
        let time = new Date();
        time.setHours(time.getHours() + 9);
        let durationSec = Math.floor((time-startTime)/1000) - totalPausedTime; // 초 단위변환
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


    // 칼로리 계산
    function calcCalories(dist, time, weight) {
        if (time < 0.5) {
            return 0; // 초기에는 칼로리 계산 제외
        }

        // 속도 계산 
        let speed = dist / (time / 60);


        // MET 값 설정 (걷기 ~ 런닝 속도에 따라 구분)
        let METs = 2.8; // 기본값: 천천히 걷기
        if (speed >= 3.0 && speed < 5.5) METs = 3.8; // 일반 걷기
        else if (speed >= 5.5 && speed < 7.0) METs = 4.3; // 빠르게 걷기
        else if (speed >= 7.0 && speed < 9.0) METs = 7.0; // 조깅
        else if (speed >= 9.0 && speed < 12.0) METs = 9.8; // 런닝
        else if (speed >= 12.0 && speed < 16.0) METs = 11.0; // 빠른 런닝
        else if (speed >= 16.0 && speed < 20.0) METs = 12.8; // 전력질주

        let calories = METs * weight * (time / 60);
        return Math.round(calories); // 반올림 후 반환

    }

    // Background Sync API 등록
    function registerBackgroundSync(path) {
        if ('serviceWorker' in navigator && 'SyncManager' in window) {
            navigator.serviceWorker.ready.then(registration => {
                registration.sync.register('syncGPSData').then(() => {
                    console.log('Background Sync 등록 완료');
                    localStorage.setItem('gpsData', JSON.stringify(path));
                }).catch(err => console.error('Background Sync 등록 실패', err));
            });
        }
    }
    
    // Service Worker 등록
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register(service_worker_url)
            .then(reg => console.log('Service Worker 등록 완료:', reg))
            .catch(err => console.log('Service Worker 등록 실패', err));
    }

    let timeUpdate = setInterval(updateTime, 1000);
    getUserGPS();

    // 백그라운드 모드 감지
    document.addEventListener("visibilitychange", function() {
        if (document.visibilityState === "hidden") {
            console.log("백그라운드 모드 진입 감지 -> Background Sync 실행");
            if('serviceWorker' in navigator && 'SyncManager' in window) {
                registerBackgroundSync(path);
            }
        }
    });

    navigator.serviceWorker.addEventListener("message", function(event) {
        if (event.data.action === "clearGPSData") {
            localStorage.removeItem('gpsData');
            console.log("localStorage GPS 데이터 삭제");
        }
        if (event.data.action === "getCSRFToken") {
            let csrfToken = getCookie("csrftoken");
            event.ports[0].postMessage({ action: "CSRFToken", token: csrfToken });
        }
        if (event.data.action === "sendGPSData") {
            let gpsData = localStorage.getItem("gpsData");
            let response = {
                action: "GPSData",
                gpsData: gpsData ? JSON.parse(gpsData) : null
            };
            // service-worker로 응답 전달
            if(event.ports && event.ports.length > 0) {
                event.ports[0].postMessage(response);
                // service worker와 클라이언트 간 응답 채널(source 사용보다 명시적)
                // ports => service worker가 응답 받기 위한 배열
            } else if (event.source) {
                event.source.postMessage(response); // 포트가 없는 경우 source 사용
            } else {
                console.error("포트가 비어있어 GPS 데이터 전송 불가");
            }
        }
    });

    document.getElementById("bottleBtn").addEventListener("click", function() {
        if (isPaused) {
            console.log("기록 수집 재개");
            isPaused = false; // 상태 변경

            let pauseStopTime = new Date();
            pauseStopTime.setHours(pauseStopTime.getHours() + 9);
            totalPausedTime += Math.floor((pauseStopTime - pauseStartTime)/1000);
            console.log(totalPausedTime); // 확인용(삭제예정)
            pauseStartTime = null; // 기록중단용 bottleBtn 클릭 시간 초기화
            getUserGPS();
            showStatus.textContent="지금은 걷는 중! 쉴 땐 물통 누르기";
        } else {
            console.log("기록 수집 중지");
            isPaused = true;

            pauseStartTime = new Date();
            pauseStartTime.setHours(pauseStartTime.getHours() + 9);
            stopUserGPS();
            showStatus.textContent="지금은 쉬는 중! 다시 걸을 땐 물통 누르기";
        }
    });

    document.getElementById("stopBtn").addEventListener("click", function() {
        let now = new Date();
        now.setHours(now.getHours() + 9); // ✅ UTC+9(KST) 변환
        let endTime = now.toISOString().slice(0, 19); // YYYY-MM-DDTHH:MM:SS 형식

        stopUserGPS();
        clearInterval(timeUpdate);

        // bottleBtn을 한번만 누른 상태에 대한 예외처리
        // 마지막 중단시간을 설정하고 totalPausedTime 업데이트
        if (isPaused && pauseStartTime) {
            let pauseStopTime = new Date();
            pauseStopTime.setHours(pauseStopTime.getHours()+9);
            totalPausedTime += Math.floor((pauseStopTime - pauseStartTime)/1000);
            console.log(totalPausedTime); // 확인용(삭제예정)
            pauseStartTime = null;
        }

        let durationSec = Math.floor((now - startTime) / 1000) - totalPausedTime; // 초 단위로 변환
        console.log(durationSec); // 확인용(삭제예정)

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
            start_time: startTime.toISOString().slice(0, 19), // ✅ 프론트에서 KST로 변환한 값 사용
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
            body: JSON.stringify(daily_record) // 서버에 JSON 형식으로 전달해야함
        })
        .then(response => response.json())
        .then(data => {
            console.log("오늘걸음 기록 저장완료:", data);
            alert(`기록이 저장되었습니다.`);
            localStorage.removeItem('gpsData');
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
