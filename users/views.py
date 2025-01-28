from django.shortcuts import render, redirect
from .models import CustomUser
import requests
from django.conf import settings
from django.contrib import messages

# Create your views here.
def login(request):
    return render(request, 'login.html')

def logout_view(request):
    """
    로그아웃 처리:
    - 네이버 로그아웃
    - 세션 초기화
    - 메인 페이지로 리디렉션
    """
    # 네이버 로그아웃 처리
    if 'naver_access_token' in request.session:
        print("네이버 로그아웃 진입")
        naver_logout(request)  # 네이버 토큰 삭제
        return redirect('users:login')  # 로그인 전 메인 페이지로 이동

    # # Google 로그아웃 처리
    # if 'google_access_token' in request.session:
    #     return google_logout(request)

    # # 일반 로그아웃 처리 (Django 세션 초기화)
    request.session.flush()

    messages.success(request, "로그아웃되었습니다.")
    return redirect('users:login')

def naver_logout(request):
    """
    네이버 로그아웃 처리:
    - 네이버 액세스 토큰 삭제
    - 세션 초기화
    """
    # 네이버 토큰 삭제 URL
    if 'naver_access_token' in request.session:
        access_token = request.session['naver_access_token']
        revoke_url = "https://nid.naver.com/oauth2.0/token"
        revoke_data = {
            'grant_type': 'delete',
            'client_id': settings.NAVER_CLIENT_ID,  # 환경 변수에서 가져옴
            'client_secret': settings.NAVER_CLIENT_SECRET,  # 환경 변수에서 가져옴
            'access_token': access_token,
            'service_provider': 'NAVER',
        }

        # 네이버 토큰 삭제 요청
        response = requests.post(revoke_url, data=revoke_data)
        response_json = response.json()

        # 토큰 삭제 성공 여부 확인
        if response_json.get('result') == 'success':
            del request.session['naver_access_token']  # 세션에서 액세스 토큰 삭제
            request.session.flush()  # Django 세션 초기화
            messages.success(request, "네이버에서 로그아웃되었습니다.")
        else:
            messages.error(request, "네이버 로그아웃 중 오류가 발생했습니다.")
    else:
        messages.error(request, "네이버 로그아웃 토큰이 없습니다.")

# 네이버 로그인 URL 생성
def naver_login(request):
    # 네이버 API의 인증 URL
    base_url = "https://nid.naver.com/oauth2.0/authorize"
    params = {
        "response_type": "code",  # OAuth 인증 코드 요청
        "client_id": settings.NAVER_CLIENT_ID,
        "redirect_uri": settings.NAVER_REDIRECT_URI,
        "state": "random_state_string",  # CSRF 방지를 위한 state 값 (임의 값)
    }
    # 파라미터를 URL 쿼리 문자열로 변환
    request_url = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return redirect(request_url)

def naver_callback(request):
    # 네이버에서 전달받은 인증 코드와 state 값
    code = request.GET.get("code")
    state = request.GET.get("state")

    # 액세스 토큰 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": settings.NAVER_CLIENT_ID,
        "client_secret": settings.NAVER_CLIENT_SECRET,
        "code": code,
        "state": state,
    }
    response = requests.post(token_url, data=payload)
    token_data = response.json()

    access_token = token_data.get("access_token")
    if access_token:
        request.session['naver_access_token'] = access_token  # 세션 저장
    else:
        return redirect('/?error=token_error')   # 오류 처리

    # 사용자 정보 요청
    user_info_url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_info_url, headers=headers)
    user_info = user_response.json().get("response")

    # 사용자 정보 추출
    email = user_info.get("email")
    nickname = user_info.get("nickname")
    user_id = user_info.get("id")

    # 사용자 정보와 함께 success.html 템플릿 렌더링
    context = {
        "email": email,
        "nickname": nickname,
        "user_id": user_id,
    }
    return render(request, "success.html", context)