let startTime;

document.getElementById("startBtn").addEventListener("click", function() {
    sessionStorage.clear(); // 기존 경로 데이터 초기화
    
    let now = new Date();
    now.setHours(now.getHours() + 9); // ✅ UTC+9(KST) 변환
    let startTime = now.toISOString().slice(0, 19); // YYYY-MM-DDTHH:MM:SS 형식

    sessionStorage.setItem("path", JSON.stringify([]));
    sessionStorage.setItem("startTime",  startTime);
    window.location.href="/record/stop/";
});