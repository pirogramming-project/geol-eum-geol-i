let startTime;

document.getElementById("startBtn").addEventListener("click", function() {
    let now = new Date();
    now.setHours(now.getHours() + 9); // ✅ UTC+9(KST) 변환
    let startTime = now.toISOString().slice(0, 19); // YYYY-MM-DDTHH:MM:SS 형식


    sessionStorage.setItem("startTime",  startTime);
    window.location.href="/record/stop/";
});