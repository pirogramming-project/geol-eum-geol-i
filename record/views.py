from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import *
from .serializers import DetailSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .form__test import RecordUpdateTestForm
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from .utils import update_monthly_record

def main_view(request):
    return render(request, 'main/landing.html')

def record_stop(request):
    return render(request, 'record/record_end.html')

def record_page(request):
    return render(request, "record/record_start.html")

def ready_record(request):
    return render(request, "record/before_record.html")

def record_delete(request, pk):
    if request.method == 'POST':
        record = Detail.objects.get(id=pk)
        record_date = record.created_at
        record.delete()
        return redirect('record:record_history', date=record_date)
    return redirect('review:record_history', date=datetime.today().strftime("%Y-%m-%d"))

def calculate_calories(distance, minutes, weight=75):
    speed = distance / (minutes / 60) if minutes > 0 else 0  # km/h 속도 계산

    # 운동 강도(METs) 값 설정
    if speed < 5.5:
        METs = 3.8  
    elif speed < 8.0:
        METs = 4.3  
    # 속도 구간에 따른 MET 값
    if speed >= 3.0 and speed < 5.5:
        METs = 3.8
    elif speed >= 5.5 and speed < 7.0:
        METs = 4.3
    elif speed >= 7.0 and speed < 9.0:
        METs = 7.0
    elif speed >= 9.0 and speed < 12.0:
        METs = 9.8
    elif speed >= 12.0 and speed < 16.0:
        METs = 11.0
    elif speed >= 16.0 and speed < 20.0:
        METs = 12.8
    else:
        METs = 7.0    
        METs = 2.8  # 기본값 (천천히 걷기)

    return int(round(METs * weight * (minutes / 60)))

#운동 종료 시, 기록 저장 함수
@login_required
@api_view(["POST"])
def save_walk_record(request):
    user = request.user
    data = request.data

    print("받은 데이터:", data, flush=True)  # 프론트에서 보낸 원본 데이터 확인

    try:
        if not isinstance(data, dict):
            data = json.loads(request.body.decode('utf-8'))
            
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        total_seconds = int(data.get("time", 0))

        if start_time and end_time:
            # 프론트에서 KST로 보내므로, UTC 변환 없이 그대로 사용!
            kst_start_dt = datetime.fromisoformat(start_time)
            kst_end_dt = datetime.fromisoformat(end_time)
        else:
            return JsonResponse({"error": "Invalid start_time or end_time"}, status=400)

        # 시, 분, 초 변환
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_str = f"{hours}h{minutes:02d}m{seconds:02d}s"

        # 거리, 속도, 칼로리 계산
        distance = float(data.get("distance", 0))
        pace = round((minutes / distance), 2) if distance > 0 else 0
        calories = round(float(data.get("calories", 0)))  # 🔹 반올림 후 저장
        path = data.get("path", [])  

        # MySQL에 저장 (UTC 변환 제거, 그대로 저장)
        walk_record = Detail.objects.create(
            user=user,
            created_at=kst_start_dt.date(),  # YYYY-MM-DD 형식
            start_time=kst_start_dt.time(),  # HH:MM:SS 형식
            end_time=kst_end_dt.time(),  # HH:MM:SS 형식
            distance=distance,
            time=time_str,
            pace=pace,
            calories=calories,
            path=path
        )

        # 월간 기록 업데이트 실행
        update_monthly_record(user)

        # JSON 변환 후 응답 반환
        serializer = DetailSerializer(walk_record)
        return JsonResponse(serializer.data, status=201)

    except Exception as e:
        print("서버 오류:", str(e), flush=True)
        return JsonResponse({"error": str(e)}, status=400)




# 기록 보여주는 함수
@login_required
def record_history(request, date):
    user = request.user  
    records = Detail.objects.filter(user=user, created_at=date).order_by("-start_time")  

    if request.method == "POST":
        record_id = request.POST.get("record_id")
        record = get_object_or_404(Detail, id=record_id, user=user)

        form = RecordUpdateTestForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect("record:record_history", date=date)

    # 페이지 네이션(한 페이지에 1개의 기록)
    paginator = Paginator(records, 1)
    page_number = request.GET.get("page", 1) # 현재 페이지 번호 가져오기
    page_obj = paginator.get_page(page_number)
    
    current_path_data = json.dumps(page_obj[0].path if page_obj else []) # 경민 추가
    
    context = {
        "date": date,  
        "records": page_obj, # 페이지네이션 적용된 객체
        "form": RecordUpdateTestForm(),
        "path_data": current_path_data, # page_obj에 해당하는 path만 전달
    }
    return render(request, "record/daily_record.html", context)


import logging
from django.contrib.auth.decorators import login_required
from .models import Detail

logger = logging.getLogger(__name__)  # 로깅 설정
# 요청한 날짜에 기록이 있는지 확인(김규일 추가)
@login_required
def check_record(request, date):
    user = request.user
    logger.info(f"check_record 요청됨 | 사용자: {user} | 요청 날짜: {date}")

    if not date or date == "undefined":
        logger.error(f"잘못된 날짜 값: {date}")
        return JsonResponse({"error": "Invalid date format"}, status=400)

    records = Detail.objects.filter(user=user, created_at=date)
    record_exists = records.exists()

    total_distance = records.aggregate(total_distance=Sum('distance'))['total_distance'] or 0
    
    logger.info(f"기록 여부: {record_exists}")
    return JsonResponse({"has_record": record_exists, "total_distance": float(total_distance)})

# 랭킹 
@login_required
def ranking_view(request):
    
    today = datetime.now() # 현재
    year = int(request.GET.get("year", today.year)) 
    month = int(request.GET.get("month", today.month))

    # 선택된 월의 전체 랭킹 조회 (정렬된 상태)
    all_rankings = list(
        Record.objects.filter(date__year=year, date__month=month)
        .select_related('user')
        .order_by('-total_distance')
    )
    
    # 상위 5명의 랭킹 리스트 생성 (순위 포함)
    rankings = [
        {"rank": index + 1, "record": record}
        for index, record in enumerate(all_rankings[:5])
    ]
    
    # ✅ 현재 로그인한 사용자의 최신 record 가져오기
    user_record = Record.objects.filter(
        user=request.user, date__year=year, date__month=month
    ).order_by('-date', '-id').first()  # 최신 데이터 한 개만 가져오기

    #현재 로그인한 유저의 순위 찾기
    user_rank = 0
    for index, record in enumerate(all_rankings, start=1):
        if record.user == request.user:
            user_rank = index
            break
    
    # 기록이 없는 경우
    if user_rank == 0 :
        user_rank = len(all_rankings) + 1
        user_record = {'total_distance': '00.00'}
        
    if user_rank <= 5 :
        is_already_in_ranking = any (
            item["record"].user == request.user for item in rankings
        ) # 사용자가 랭킹에 있는지 확인
        if not is_already_in_ranking:
            rankings.append({"rank": user_rank, "record": user_record})


    selected_date = datetime(year,month,1) # 선택된 월의 첫날
    prev_date = (selected_date - timedelta(days=1)) # 이전 달의 마지막 날
    # ✅ 다음 달의 마지막 날을 구하는 로직
    if month == 12:  # 12월이면 다음 해의 1월로 이동
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1
    
    return render(request, 'record/ranking.html', {
        'rankings': rankings,
        'user_rank': user_rank,
        "user_record" : user_record,
        'selected_year': year,
        'selected_month': month,
        'prev_year': prev_date.year,
        'prev_month': prev_date.month,
        "next_year":  next_year,
        "next_month" : next_month
    })
    
    
    