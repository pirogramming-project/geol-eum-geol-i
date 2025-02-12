// 캘린더 관련 DOM 요소 가져오기
const calendarDates = document.getElementById("calendarDates");
const currentMonthElement = document.getElementById("currentMonth");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

const totalDistanceElement = document.getElementById("totalDistance");
const totalCaloriesElement = document.getElementById("totalCalories");

// 현재 날짜 정보 설정
const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

// 캘린더를 렌더링하는 함수
function renderCalendar() {
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const startDayOfWeek = firstDayOfMonth.getDay();
    currentMonthElement.textContent = `${currentYear}년 ${currentMonth + 1}월`;

    // 캘린더 날짜 초기화
    calendarDates.innerHTML = "";

    // 빈 날짜 (이전 달)
    for (let i = 0; i < startDayOfWeek; i++) {
        const emptyDate = document.createElement("div");
        emptyDate.classList.add("date", "empty");
        calendarDates.appendChild(emptyDate);
    }

    // 현재 달 날짜 생성
    for (let i = 1; i <= daysInMonth; i++) {
        const dateElement = document.createElement("div");
        dateElement.classList.add("date");
        dateElement.textContent = i;

        // YYYY-MM-DD 형식으로 변환
        const formattedDate = `${currentYear}-${(currentMonth + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`;
        dateElement.dataset.date = formattedDate;
        calendarDates.appendChild(dateElement);

        // 해당 날짜의 기록 확인 후 아이콘 표시
        checkRecordAndShowIcon(dateElement, formattedDate);
    }

    // 월간 기록 업데이트
    updateMonthlyRecord();
}

// 해당 날짜의 기록 확인 후 아이콘을 표시하는 함수
function checkRecordAndShowIcon(dateElement, date) {
    fetch(`/record/check/${date}/`)
        .then(response => response.json())
        .then(data => {
        if (data.has_record) {
            dateElement.classList.add("record-exists"); // 레코드가 있으면 스타일 추가
            const svgIcon = document.createElement("div");
            svgIcon.classList.add("icon-overlay");

            let opacityClass = "";

            if (0 < data.total_distance && data.total_distance <= 1) {
            opacityClass = "opacity-0-25";
            } else if (1 < data.total_distance && data.total_distance <= 3) {
            opacityClass = "opacity-0-50";
            } else if (3 < data.total_distance && data.total_distance <= 5) {
            opacityClass = "opacity-0-75";
            } else if (0 === data.total_distance) {
            opacityClass = "opacity-0";
            } else {
            opacityClass = "opacity-1";
            }

            svgIcon.classList.add(opacityClass);

            console.log(`날짜: ${date}, 거리: ${data.total_distance}, 설정된 opacity: ${opacityClass}`);
            
            svgIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="65" height="78" viewBox="0 0 65 78" fill="none">
            <path d="M41.718 32.3128C41.9503 31.6808 42.3389 24.7092 46.0826 19.7368C50.4654 13.9163 44.7557 8.29626 38.5975 8.29626C31.3838 8.31883 32.3057 14.5975 26.38 21.0345C26.3754 21.0345 26.3754 21.0345 26.3754 21.039C21.689 24.8375 15.2064 30.0553 17.6671 35.6846C20.8336 42.0176 23.86 46.292 26.6262 49.1358C19.6009 53.1419 19.2724 52.9997 19.4726 53.3427C19.6957 53.7354 19.9509 53.1734 26.9253 49.4337C27.2518 49.7655 27.5807 50.0769 27.9026 50.3658C16.7777 56.5452 17.3776 56.0985 17.5318 56.3603C17.587 56.4573 17.7158 56.4912 17.8147 56.437C28.7488 50.3386 28.1325 50.7631 28.1831 50.6211C28.7557 51.1176 29.3168 51.5532 29.8548 51.9346C23.6231 55.4939 23.2139 55.4013 23.4117 55.7444C23.5681 56.0107 23.2623 56.0491 30.2322 52.1897C30.6553 52.4741 31.0646 52.7133 31.4647 52.93C21.3259 58.6716 21.1882 58.4211 21.3883 58.7644C21.616 59.1616 21.6942 58.6876 31.9015 53.1604C32.7064 53.5576 33.4721 53.842 34.1942 54.0315C27.5138 57.8413 27.1418 57.7329 27.3349 58.076C27.5625 58.4619 27.8063 57.9067 34.7875 54.167C45.4621 56.3314 50.238 39.5307 41.4514 42.7039C41.2904 42.7264 40.8788 42.9273 40.6006 42.6881C39.9682 42.1419 40.4396 39.9797 40.412 39.8601C40.6742 38.2487 40.7568 34.9396 41.718 32.3128ZM38.8367 41.5029C39.2024 41.2253 39.4484 40.7671 39.6761 41.0064C39.9083 41.2524 39.4254 41.4645 39.1196 41.8031C38.9195 41.9859 38.6367 41.688 38.8367 41.5029ZM39.3748 39.6477C39.4576 39.5665 39.591 39.571 39.6692 39.6522C39.9014 39.8915 39.4185 40.1036 39.1196 40.4489C39.0368 40.5256 38.8643 40.4805 38.8252 40.4376C38.5907 40.1984 39.0759 39.9862 39.3748 39.6477ZM39.1081 36.312C38.9241 36.312 38.8298 36.0885 38.9632 35.9576C39.3242 35.6845 39.5749 35.2219 39.8026 35.4611C39.8853 35.5423 39.8807 35.6732 39.798 35.75C39.2806 36.2081 39.253 36.312 39.1081 36.312ZM39.1426 37.7135C39.0529 37.7948 38.9264 37.7903 38.8482 37.709C38.616 37.4698 39.1035 37.2509 39.4047 36.9123C39.5427 36.7859 39.6761 36.8311 39.7427 36.9168C39.9083 37.147 39.5473 37.2825 39.1426 37.7135ZM38.8298 38.7991C39.1909 38.5215 39.4415 38.0634 39.6692 38.3026C39.9014 38.5418 39.4185 38.754 39.1196 39.0925C39.0368 39.1738 38.9034 39.1693 38.8253 39.088C38.7425 39.0045 38.7471 38.8736 38.8298 38.7991ZM38.6252 8.70498C44.2062 8.70498 50.0149 13.8238 45.7511 19.4979C43.1849 22.8991 41.881 27.8439 41.3406 32.0738C38.7743 32.6561 35.6976 31.0333 34.8605 27.6637C33.9889 24.1587 30.4339 23.4997 26.858 21.1233C32.6206 14.614 31.8387 8.70568 38.6245 8.70568L38.6252 8.70498Z" fill="#6A3200" fill-opacity="0.6"/>
            <path d="M25.7134 60.6511C25.4742 60.782 25.6812 61.1408 25.9181 61.0054C36.3648 55.1011 36.4754 55.363 36.2753 55.0202C36.0821 54.6704 36.2542 54.9049 25.7134 60.6511Z" fill="#6A3200" fill-opacity="0.6"/>
            </svg>
            `;
            dateElement.appendChild(svgIcon); // SVG 아이콘을 날짜에 추가
        }
        })
        .catch(error => console.error("에러 발생:", error));
    }

// AJAX 요청 시, 정확한 URL 패턴 사용
function updateMonthlyRecord() {
    const url = `/course/record/calendar/${currentYear}/${currentMonth + 1}/`;  // URL 변수에 저장

    console.log(`Fetching monthly record: ${url}`);

    fetch(url)
        .then(response => {
            if (!response.ok) {
                console.error(`서버 오류: ${response.status}`);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();  // JSON으로 변환
        })
        .then(data => {
            console.log(`데이터 수신: 거리=${data.total_distance}, 칼로리=${data.total_calories}`);
            document.getElementById("totalDistance").textContent = `${data.total_distance}`;
            document.getElementById("totalCalories").textContent = `${data.total_calories}`;
        })
        .catch(error => console.error("이달의 기록을 가져오는 중 오류 발생:", error));
}


// 이전 달 보기 버튼 클릭 이벤트
prevBtn.addEventListener("click", () => {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
});

// 다음 달 보기 버튼 클릭 이벤트
nextBtn.addEventListener("click", () => {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar();
});

// 캘린더 날짜 클릭 시 상세 기록 페이지로 이동
document.addEventListener("DOMContentLoaded", function () {
    const dates = document.getElementById("calendarDates");

    dates.addEventListener("click", function (event) {
        if (event.target.classList.contains("date")) {
            const selectedDate = event.target.dataset.date; // 선택한 날짜 가져오기
            console.log("선택된 날짜:", selectedDate); // 디버깅 로그 출력

            if (!selectedDate) {
                alert("날짜 정보가 올바르게 전달되지 않았습니다.");
                return;
            }

            // 선택한 날짜의 기록 존재 여부 확인 후 페이지 이동
            fetch(`/record/check/${selectedDate}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.has_record) {
                        window.location.href = `/record/history/${selectedDate}/`;
                    } else {
                        alert("이 날짜에는 기록이 없습니다.");
                    }
                })
                .catch(error => console.error("에러 발생:", error));
        }
    });
});

// 초기 캘린더 렌더링 실행
renderCalendar();
