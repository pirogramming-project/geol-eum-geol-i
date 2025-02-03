let startTime;

document.getElementById("startBtn").addEventListener("click", function() {
    //startTime = new Date().toISOString(); // ISO 형식으로 저장
    let now = new Date();
    now.setHours(now.getHours() + 9); // ✅ UTC+9(KST) 변환
    let startTime = now.toISOString().slice(0, 19); // YYYY-MM-DDTHH:MM:SS 형식


    sessionStorage.setItem("startTime",  startTime);
    window.location.href="/record/stop/";
});