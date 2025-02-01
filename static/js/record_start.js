let startTime, watchID, path = [];

document.getElementById("startBtn").addEventListener("click", function() {
    startTime = new Date().getTime();
    path = [];

    if(navigator.geolocation) {
        watchID = navigator.geolocation.watchPosition(
            (position) => {
                path.push({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    timestamp: position.timestamp
                });
            },
            (error) => console.error("Error getting GPS: ", error),
            { enableHighAccuracy: true, maximumAge: 0, timeout: 5000}
        );
    }

    localStorage.setItem("startTime",  startTime);
    // localStorage => 다른 페이지로 이동해도 해당 값 공유가능
});