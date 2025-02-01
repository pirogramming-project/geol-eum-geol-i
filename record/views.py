from django.shortcuts import render

def main_view(request):
    return render(request, 'main/landing.html')

def record_start(request):
    return render(request, 'record/record_start.html')

def record_stop(request):
    return render(request, 'record/record_end.html')