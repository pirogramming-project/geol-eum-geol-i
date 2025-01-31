from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Course, Keyword, CourseKeyword
from .forms import CourseForm
from decimal import Decimal
from .utils import calculate_distance
import json

def course_list(request):
    search_term = request.GET.get('search', '')  # URL에서 'search' 파라미터를 가져옵니다.
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    selected_location = None

    # 위도와 경도가 제공되었을 때
    if latitude and longitude:
        selected_location = (float(latitude), float(longitude))

    # 검색어가 있을 경우 'title' 필드에서 검색어가 포함된 항목을 찾음
    if search_term:
        courses = Course.objects.filter(title__icontains=search_term)
    else:
        courses = Course.objects.all()

    # 3km 이내의 코스만 필터링
    if selected_location:
        courses = [
            course for course in courses
            if course.start_location and calculate_distance(
                selected_location[0], selected_location[1],
                course.start_location['latitude'], course.start_location['longitude']
            ) <= 3
        ]

    # 페이지네이션 처리
    paginator = Paginator(courses, 15)  # 페이지당 15개 항목
    page_number = request.GET.get('page', 1)  # 현재 페이지 번호, 없으면 1로 설정
    page_obj = paginator.get_page(page_number)

    # 페이지네이션 정보와 검색어를 전달
    return render(request, 'wherewalk/courserecommand.html', {
        'page_obj': page_obj,
        'search_term': search_term,  # 검색어를 템플릿으로 전달
    })

class CourseDetailView(DetailView):
    model = Course
    template_name = 'wherewalk/course_detail.html'  # 사용할 템플릿 파일
    context_object_name = 'course'  # 템플릿에서 사용할 변수 이름

def calendar_view(request):
    return render(request, 'calendarpage/calendar.html')

def course_form_view(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        selected_keywords = request.POST.getlist("keywords")

        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user  # 현재 로그인한 사용자 저장
            course.distance = 0
            course.time = 0
            course.start_location = None
            course.save()

            # 선택한 키워드 저장
            for keyword_name in selected_keywords:
                keyword, created = Keyword.objects.get_or_create(name=keyword_name)
                CourseKeyword.objects.create(course=course, keyword=keyword)

            return redirect("course_form")  # 폼 제출 후 다시 폼 페이지로 이동

    else:
        form = CourseForm()

    return render(request, "wherewalk/course_form.html", {"form": form})

def submit_course(request):
    if request.method == "POST":
        try:
            print("📌 submit_course 실행됨!")

            # 폼 데이터를 가져오기
            title = request.POST.get("title")
            distance = Decimal(request.POST.get("distance"))  # Decimal 변환
            time = int(request.POST.get("time"))  # 정수 변환
            image = request.FILES.get("image")
            keywords = json.loads(request.POST.get("keywords", "[]"))  # JSON 변환

            # 먼저 latitude, longitude 값을 가져오기
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")

            # 디버깅 출력: latitude와 longitude 값을 먼저 확인
            print(f"📌 title: {title}, distance: {distance}, time: {time}, lat: {latitude}, lng: {longitude}")

            # 위치 정보 처리 (JSON 변환)
            start_location = {
                "latitude": float(latitude) if latitude else None,
                "longitude": float(longitude) if longitude else None
            }

            # Course 객체 생성
            course = Course.objects.create(
                user=request.user,
                title=title,
                distance=distance,
                time=time,
                start_location=start_location,
                image=image
            )

            # 키워드 저장
            for keyword_name in keywords:
                keyword, created = Keyword.objects.get_or_create(name=keyword_name)
                CourseKeyword.objects.create(course=course, keyword=keyword)

            return JsonResponse({"message": "코스가 성공적으로 저장되었습니다."})

        except (ValueError, TypeError) as e:
            return JsonResponse({"error": f"잘못된 입력 값: {str(e)}"}, status=400)

    return JsonResponse({"error": "잘못된 요청"}, status=400)