window.onload = function () {
    const modal = document.getElementById("profile-modal");
    const openModalBtn = document.getElementById("open-modal");
    const closeModalBtn = document.querySelector(".close-modal");
    const profilePreview = document.getElementById("modal-profile-preview");
    const fileInput = document.getElementById("profile-upload");

    // 페이지 로드 시 모달 숨기기
    modal.style.display = "none";

    if (openModalBtn) {
        // 모달 열기
        openModalBtn.addEventListener("click", function (event) {
            event.preventDefault();
            modal.style.display = "flex";
        });
    } else {
        console.error("openModalBtn 요소를 찾을 수 없습니다.");
    }

    // 모달 닫기
    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    // 파일 선택 시 이미지 미리보기
    if (fileInput) {
        fileInput.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profilePreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
};
