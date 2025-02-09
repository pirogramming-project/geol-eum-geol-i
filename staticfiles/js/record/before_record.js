document.addEventListener("DOMContentLoaded", function() {
    let countdownElement = document.getElementById("ready_countdown");
    let outerCircle = document.querySelector(".before__r_outer_circle");
    let innerCircle = document.querySelector(".before__r_inner_circle");
    let innerNumber = document.querySelector(".before__r_countdown");
    let countdown = 4;

    function updateCountdown() {
        if( countdown > 1 ) {
            countdown -= 1;
            countdownElement.textContent = countdown;

            outerCircle.style.transform = "scale(1.4)";
            setTimeout(() => {
                outerCircle.style.transform = "scale(1)";
            }, 450);

            setTimeout(updateCountdown, 1000); // 재귀함수
        } else {
            setTimeout(() => {
                window.location.href = "/record/stop/";
            }, 300);
        }
    }

    setTimeout(updateCountdown); // 1초 후 시작
});