let startTime;

document.getElementById("startBtn").addEventListener("click", function() {
    startTime = new Date().toISOString(); // ISO 형식으로 저장

    sessionStorage.setItem("startTime",  startTime);
    window.location.href="/record/stop/";
});