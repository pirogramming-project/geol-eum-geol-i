setTimeout(() => {
    document.body.style.animation = "fadeOut 1s forwards";
    setTimeout(() => {
        window.location.href = "/main/";
    }, 1000);
}, 2000);