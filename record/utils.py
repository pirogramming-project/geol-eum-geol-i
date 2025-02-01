from datetime import datetime
from django.db.models import Sum
from .models import Detail, Record

def update_monthly_record(user):
    """현재 월의 총 이동 거리와 칼로리를 `Record` 모델에 저장"""
    today = datetime.today()
    year, month = today.year, today.month

    # 현재 월을 `date`로 저장할 값 설정
    month_date = datetime(year, month, 1).date()  # YYYY-MM-01

    # 현재 월의 총 이동 거리와 총 소모 칼로리 계산
    stats = Detail.objects.filter(
        user=user, created_at__year=year, created_at__month=month
    ).aggregate(total_distance=Sum("distance"), total_calories=Sum("calories"))

    total_distance = stats["total_distance"] or 0
    total_calories = stats["total_calories"] or 0

    # `Record`에 월 정보 저장 (있으면 업데이트, 없으면 새로 생성)
    record, created = Record.objects.get_or_create(user=user, date=month_date)
    record.total_distance = total_distance
    record.total_calories = total_calories
    record.save()
