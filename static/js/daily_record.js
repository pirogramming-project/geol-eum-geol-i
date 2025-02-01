document.getElementById("walkForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append("walkImage", document.getElementById("walkImage").files[0]);
    formData.append("walkComment", document.getElementById("walkComment").value);

    let response = await fetch("/save_record", {
        method: "POST",
        body: formData
    });

    if(response.ok) {
        alert("✅ 최종등록이 반영되었습니다.");
        loadWalkData();
    } else {
        alert("최종등록에 문제가 생겼습니다. 다시 시도해주세요🥲");
    }
});

async function loadWalkData() {
    let response = await fetch("/load_record");
    let data = await response.json();

    let walkDatas = document.getElementById("walkDatas");
    walkDatas.innerHTML =`
    <div class="daily__image">
        <img src="" alt="오늘걸음 이미지">
    </div>
    <div class="daily__comment">
        <p></p>
    </div>
    `;
}

window.onload = loadWalkData;