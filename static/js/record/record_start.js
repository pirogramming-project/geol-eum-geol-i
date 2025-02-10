document.addEventListener("DOMContentLoaded", function() {
    const recordDate = document.querySelector(".record__date");
    if(recordDate) {
        const today = new Date();
        // month: 0~11로 저장되어있음
        const formattedDate = today.getFullYear() + "." +
            String(today.getMonth() + 1).padStart(2, '0') + "." +
            String(today.getDate()).padStart(2, '0');
        recordDate.textContent = formattedDate;
    }
});

document.getElementById("startBtn").addEventListener("click", function() {
    window.location.href="/record/ready/";
});