from django.shortcuts import render
from django.views.generic import DetailView
from django.core.paginator import Paginator
from .models import Course

def course_list(request):
    search_term = request.GET.get('search', '')  # URL에서 'search' 파라미터를 가져옵니다.

    # 검색어가 있을 경우 'title' 필드에서 검색어가 포함된 항목을 찾음
    if search_term:
        courses = Course.objects.filter(title__icontains=search_term)
    else:
        courses = Course.objects.all()

    # 페이지네이션 처리
    paginator = Paginator(courses, 15)  # 페이지당 15개 항목
    page_number = request.GET.get('page', 1)  # 현재 페이지 번호, 없으면 1로 설정
    page_obj = paginator.get_page(page_number)

    # 페이지네이션 정보와 검색어를 전달
    return render(request, 'courserecommand.html', {
        'page_obj': page_obj,
        'search_term': search_term,  # 검색어를 템플릿으로 전달
    })

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'  # 사용할 템플릿 파일
    context_object_name = 'course'  # 템플릿에서 사용할 변수 이름

def calendar_view(request):
    return render(request, 'calendar.html')