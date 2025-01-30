from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# 전체 기록 (한달 단위)
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_distance = models.DecimalField(max_digits=6, decimal_places=2)  # 총 이동 거리 (KM)
    total_time = models.PositiveIntegerField()  # 총 이동 시간 (분)
    avg_pace = models.DecimalField(max_digits=4, decimal_places=2)  # 평균 페이스 (분/km)
    total_calories = models.PositiveIntegerField()  # 총 소모 칼로리

    def __str__(self):
        return f"{self.user.nickname} - {self.total_distance}km"

# 개별 기록 (그날의 기록)
class Detail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)  # 운동 날짜
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # 이동 거리 (KM)
    time = models.PositiveIntegerField()  # 이동 시간 (분)
    pace = models.DecimalField(max_digits=4, decimal_places=2)  # 페이스 (분/km)
    calories = models.PositiveIntegerField()  # 소모 칼로리
    memo = models.TextField(null=True, blank=True)  # 메모
    path = models.JSONField(null=True, blank=True)  # 이동 경로 데이터 (좌표 JSON 형태)

    def __str__(self):
        return f"{self.user.nickname} - {self.created_at}"
