from django.shortcuts import render

def main_view(request):
    return render(request, 'main/landing.html')

def record_start(request):
    return render(request, 'record/record_start.html')

def record_stop(request):
    return render(request, 'record/record_end.html')

def daily_record(request):
    return render(request, 'record/daily_record.html')

# def save_record(request): - 사진/코멘트 저장하는 함수 필요
# def load_record(request): - 사진/코멘트 보내는(불러오는) 함수 필요