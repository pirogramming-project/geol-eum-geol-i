from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from datetime import datetime
from .models import *
from .serializers import DetailSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .form__test import RecordUpdateTestForm
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta

def main_view(request):
    return render(request, 'main/landing.html')

def record_stop(request):
    return render(request, 'record/record_end.html')

def daily_record(request):
    return render(request, 'record/daily_record.html')

def record_page(request):
    return render(request, "record/record_start.html")

# 칼로리 계산 
def calculate_calories(distance, minutes, weight=75):  # 체중 기본값 75kg
    speed = distance / (minutes / 60) if minutes > 0 else 0  # km/h 속도 계산

    # 운동 강도(METs) 값 설정
    if speed < 5.5:
        METs = 3.8  
    elif speed < 8.0:
        METs = 4.3  
    else:
        METs = 7.0    

    return int(round(METs * weight * (minutes / 60)))


#@login_required
@api_view(["POST"])  # POST 요청만 허용
#운동 종료 시, 기록 저장 함수
@api_view(["POST"])
def save_walk_record(request):
    user = request.user
    data = request.data

    print("🚀 받은 데이터:", data, flush=True)  # ✅ 프론트에서 보낸 원본 데이터 확인

    try:
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if start_time and end_time:

            # ✅ 프론트에서 KST로 보내므로, UTC 변환 없이 그대로 사용!
            kst_start_dt = datetime.fromisoformat(start_time)
            kst_end_dt = datetime.fromisoformat(end_time)

            # 🔹 총 운동 시간 계산 (초 단위)
            total_seconds = int((kst_end_dt - kst_start_dt).total_seconds())
        else:
            total_seconds = 0

        # 🔹 시, 분, 초 변환
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_str = f"{hours}h{minutes:02d}m{seconds:02d}s"

        # 🔹 거리, 속도, 칼로리 계산
        distance = float(data.get("distance", 0))
        pace = round((minutes / distance), 2) if distance > 0 else 0
        calories = calculate_calories(distance, minutes)
        path = data.get("path", [])  

        # 🔹 MySQL에 저장 (UTC 변환 제거, 그대로 저장)
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

        # 🔹 JSON 변환 후 응답 반환
        serializer = DetailSerializer(walk_record)
        return Response(serializer.data, status=201)

    except Exception as e:
        print("🚨 서버 오류:", str(e), flush=True)
        return Response({"error": str(e)}, status=400)



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


    context = {
        "date": date,  
        "records": records,
        "form": RecordUpdateTestForm(),
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

    record_exists = Detail.objects.filter(user=user, created_at=date).exists()
    
    logger.info(f"기록 여부: {record_exists}")
    return JsonResponse({"has_record": record_exists})

from .utils import update_monthly_record  # 새로 만든 함수 가져오기

# 걷기 기록이 추가 기능 걷기 기능 만들 때 참고(김규일)
@api_view(["POST"])
def save_walk_record(request):
    user = request.user
    data = request.data
    print("받은 데이터:", data)

    try:
        start_time = data.get("start_time", None)
        end_time = data.get("end_time", None)
        
        if start_time and end_time:
            start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            total_seconds = int((end_dt - start_dt).total_seconds()) 
        else:
            total_seconds = 0 

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_str = f"{hours}h{minutes:02d}m{seconds:02d}s"

        distance = float(data.get("distance",0))
        pace = round((minutes / distance),2) if distance > 0 else 0 
        calories = calculate_calories(distance, minutes)
        path = data.get("path",[]) 

        # 운동 기록 저장
        walk_record = Detail.objects.create(
            user=user,
            created_at=start_dt.date(),
            start_time=start_dt.time(),
            end_time=end_dt.time(),
            distance=distance,
            time=time_str,
            pace=pace,
            calories=calories,
            path=path
        )

        # `Record` 업데이트
        update_monthly_record(user)

        serializer = DetailSerializer(walk_record)
        return Response(serializer.data, status=201)

    except Exception as e:
        print("서버 오류:", str(e))
        return Response({"error": str(e)}, status=400)
