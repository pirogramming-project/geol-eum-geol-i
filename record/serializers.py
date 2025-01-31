from rest_framework import serializers
from .models import *

# serializers.py 파일은 Python 객체(모델 인스턴스)를 JSON 형식으로 변환하는 역할
# serializers.ModelSerializer : ModelSerializer를 사용하면 Django 모델(Detail)을 JSON 형식으로 변환하는 과정이 자동화됨

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail      # 🚀 직렬화할 모델 지정
        fields = "__all__"   # 🚀 모든 필드를 JSON으로 변환
        