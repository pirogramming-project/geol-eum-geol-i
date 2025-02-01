from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# 코스 정보 (장소 추천)
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # 총 거리 (KM)
    time = models.PositiveIntegerField()  # 예상 소요 시간 (분)
    start_location = models.JSONField(null=True, blank=True)  # 출발 위치
    image = models.ImageField(upload_to="course_images/", null=True, blank=True)  # 이미지 파일
    description = models.CharField(max_length=70, blank=True, null=True)  # 70

    def __str__(self):
        return self.title

# 추천 해시태그
class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 해시태그 이름

    def __str__(self):
        return self.name

# 코스-해시태그 연결 (다대다 관계)
class CourseKeyword(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "keyword")  # 동일한 연결 방지

    def __str__(self):
        return f"{self.course.title} - {self.keyword.name}"

