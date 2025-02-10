// 백그라운드 모드에서 GPS 데이터를 서버로 전송하는 역할
self.addEventListener('install', event => {
    console.log('Service Worker 설치됨');
    self.skipWaiting(); // 즉시 활성화
});

self.addEventListener('activate', event => {
    console.log('Service Worker 활성화');
    return self.clients.claim();
});

// Background Sync 이벤트 감지
self.addEventListener('sync', event => {
    if(event.tag === 'syncGPSData') {
        console.log('Background Sync 감지됨 -> GPS 데이터 전송 시작');
        event.waitUntil(sendGPSDataToServer());
    }
});

// 저장된 GPS 데이터를 서버로 전송
async function sendGPSDataToServer() {
    try {
        let gpsData = await getGPSDataFromClient();
        if (!gpsData) {
            console.log('저장된 GPS 데이터 없음');
            return;
        }

        let response = await fetch('/record/save_walk_record/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': await getCSRFToken()
            },
            body: JSON.stringify({ path:gpsData })
        });

        if(response.ok) {
            console.log('GPS 데이터 전송완료');
            // 서버로 데이터 전송 후 클라이언트에 삭제 요청
            self.clients.matchAll().then(clients => {
                clients.forEach(client => client.postMessage({ action: "clearGPSData" }));
            });
        } else {
            console.error('GPS 데이터 전송 실패');
            self.clients.matchAll().then(clients => { 
                setTimeout(() => {
                    clients.forEach(client => client.postMessage({ action: "clearGPSData" }));
                }, 300000); // 5분 후 localStorage GPS 데이터 삭제
            });
        }
    } catch (error) {
        console.error('백그라운드 모드 GPS 데이터 전송 중 오류 발생', error);
        self.clients.matchAll().then(clients => {
            setTimeout(() => {
                clients.forEach(client => client.postMessage({ action: "clearGPSData" }));
            }, 300000); // 5분 후 localStorage GPS 데이터 삭제
        });
    }
}

// LocalStorage(백그라운드 모드에서 GPS 데이터 저장한 곳)에서 GPS 데이터 가져오기
async function getGPSDataFromClient() {
    return new Promise(resolve => {
        // 현재 활성화된 클라이언트(페이지) 조회
        self.clients.matchAll().then(clients => {
            if(clients.length === 0) {
                resolve(null); // client 없으면 null 반환
                return;
            }
            // 클라이언트에 GPS 데이터 요청
            clients[0].postMessage({ action: "sendGPSData" });
            // 응답 대기
            self.addEventListener("message", function(event) {
                if (event.data.action === "GPSData") {
                    resolve(event.data.gpsData);
                }
            });
        });
    });
}

// csrf 토큰 가져오기
async function getCSRFToken() {
    let clients = await self.clients.matchAll();
    for (let client of clients) {
        client.postMessage({action: "getCSRFToken"});
    }
    return new Promise(resolve => {
        self.addEventListener("message", function(event) {
            if (event.data.action === "CSRFToken") {
                resolve(event.data.token);
            }
        });
    });
}