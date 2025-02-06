document.getElementById("startBtn").addEventListener("click", function() {
    sessionStorage.clear(); // 기존 경로 데이터 초기화

    sessionStorage.setItem("path", JSON.stringify([]));
    window.location.href="/record/ready/";
});