document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("profile-modal");
  const openModalBtn = document.getElementById("open-modal");
  const closeModalBtn = document.querySelector(".close-modal");
  const profilePreview = document.getElementById("modal-profile-preview");
  const fileInput = document.getElementById("profile-upload");
  const navBar = document.querySelector(".bottom_nav");

  // 페이지가 완전히 로딩될 때까지 숨김 처리
  modal.style.display = "none";
  navBar.style.filter = "brightness(100%)";
  document.body.style.visibility = "hidden"; // 페이지 깜빡임 방지

  window.onload = function () {
    document.body.style.visibility = "visible"; // 로딩 완료 후 다시 보이게
  };

  if (openModalBtn) {
    // 모달 열기
    openModalBtn.addEventListener("click", function (event) {
      event.preventDefault();
      modal.style.display = "flex";
      navBar.style.filter = "brightness(50%)";
    });
  } else {
    console.error("openModalBtn 요소를 찾을 수 없습니다.");
  }

  // 모달 닫기
  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", function () {
      modal.style.display = "none";
      navBar.style.filter = "brightness(100%)";
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
});
