from django.shortcuts import render, redirect             # 템플릿 렌더링 및 URL 리다이렉션을 위한 도구
from .models import CustomUser                            # CustomUser 모델 (사용자 데이터베이스 모델)
import requests                                           # 외부 API 호출 (예: 소셜 로그인)
from django.conf import settings                          # Django 프로젝트 설정값 호출
from django.contrib import messages                      # Django 메시지 프레임워크 (알림, 에러 메시지 처리)
from django.http import JsonResponse                     # JSON 응답을 생성하기 위한 도구
from .forms import CustomUserCreationForm                # 사용자 생성 폼 (회원가입 폼)
from django.contrib.auth import authenticate, login, logout  # 사용자 인증, 로그인 및 로그아웃 관리

# 이메일 인증 관련 도구들
from django.contrib.sites.shortcuts import get_current_site  # 현재 사이트 정보를 가져오기 (도메인 포함)
from django.template.loader import render_to_string          # 템플릿을 문자열로 렌더링
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode        # UID를 Base64로 인코딩 (보안 토큰 생성용)
from django.utils.encoding import force_bytes, force_str                 # 데이터를 바이트로 변환 (Base64 인코딩에 필요)
from django.http import HttpResponse                        # HTTP 응답 생성
from django.core.mail import send_mail                      # 이메일 전송 도구
from .utils import email_verification_token                 # 이메일 인증 토큰 생성 유틸리티
from django.contrib.auth import get_user_model             # 사용자 모델 가져오기 (커스텀 유저 지원)      # Base64로 인코딩된 UID를 디코딩         # 데이터를 문자열로 강제 변환
from django.contrib.auth.tokens import default_token_generator
import json
import uuid
from django.core.cache import cache
from django.utils.timezone import now
from datetime import datetime, timedelta

# 마이페이지
from django.db import connection
from django.contrib.auth.decorators import login_required
from .forms import ProfileImageForm


def landing_view(request):
    return render(request, 'main/landing.html')

def main_beforeLogin(request):
    return render(request, 'main/main(beforeLogin).html')



User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # user_id 대신 email 사용
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  # 이메일로 인증

        if user is not None:
            login(request, user)
            return redirect('users:success')
        else:
            return render(request, 'UserManage/login.html', {'error': 'Invalid Email or Password'})

    return render(request, 'UserManage/login.html')

def success_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')  # 로그인되지 않았다면 로그인 페이지로 리다이렉트

    return render(request, 'main/main(afterLogin).html', {'user': request.user})

'''
회원가입 view
'''
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            nickname = form.cleaned_data['nickname']

            # 캐시에 계정 정보 저장 (이메일 인증 후 계정 생성)
            temp_user_data = {
                'email': email,
                'password': password,
                'nickname': nickname,
            }
            cache_key = f"signup_{email}"  # 이메일 기반 캐시 키
            cache.set(cache_key, json.dumps(temp_user_data), timeout=600)  # 10분 동안 저장

            # 이메일 인증을 위한 토큰 생성
            token = default_token_generator.make_token(User(email=email))
            uid = urlsafe_base64_encode(force_bytes(email))  # 이메일을 기반으로 직렬화

            # 이메일 인증 메일 발송
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('UserManage/activate_email.html', {
                'uid': uid,
                'domain': current_site.domain,
                'token': token,
            })
            send_mail(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"message": "이메일이 전송되었습니다! 이메일을 확인해주세요!"})

        # 유효성 검사 실패 시 오류 메시지 반환
        return JsonResponse({"error": form.errors}, status=400)

    return render(request, 'UserManage/signup.html', {'form': CustomUserCreationForm()})



def activate(request, uidb64, token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))  # 이메일 기반 디코딩
        cache_key = f"signup_{email}"
        temp_user_data_json = cache.get(cache_key)

        if not temp_user_data_json:
            return render(request, "UserManage/FindPassword/password_reset_invalid.html")

        temp_user_data = json.loads(temp_user_data_json)

        # 이메일 인증을 위한 유효성 검사
        if not default_token_generator.check_token(User(email=email), token):
            return render(request, "UserManage/FindPassword/password_reset_invalid.html")

        # 인증 성공 후 계정 생성
        user = User.objects.create_user(
            email=temp_user_data['email'],
            password=temp_user_data['password'],
            nickname=temp_user_data['nickname'],
            is_active=True  # 인증 후 활성화
        )

        # 캐시에서 데이터 삭제
        cache.delete(cache_key)

        return render(request, "UserManage/SignUp_confirm.html")

    except (ValueError, TypeError):
        return render(request, "UserManage/FindPassword/password_reset_invalid.html")

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "해당 이메일이 존재하지 않습니다."}, status=400)

        # **토큰 및 UID 생성**
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # **토큰 생성 시간 저장 (10분 동안 유지)**
        cache_key = f"password_reset_{user.pk}"
        cache.set(cache_key, now().isoformat(), timeout=600)  # 600초 = 10분

        # **이메일 보내기**
        mail_subject = "비밀번호 재설정 링크"
        message = render_to_string("UserManage/FindPassWord/password_reset_email.html", {
            "uid": uid,
            "token": token,
            "domain": request.get_host(),
        })
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])

        return JsonResponse({"message": "비밀번호 재설정 링크가 이메일로 전송되었습니다!"})

    return render(request, "UserManage/FindPassWord/password_reset.html")

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # **토큰 검증**
        if not default_token_generator.check_token(user, token):
            return render(request, "UserManage/FindPassword/password_reset_invalid.html")

        # **캐시에서 토큰 생성 시간 가져오기**
        cache_key = f"password_reset_{user.pk}"
        token_created_at_str = cache.get(cache_key)

        if not token_created_at_str:
            return render(request, "UserManage/FindPassword/password_reset_invalid.html")

        # **토큰 생성 시간을 datetime으로 변환 후 10분 초과 확인**
        token_created_at = datetime.fromisoformat(token_created_at_str)
        token_valid_duration = timedelta(minutes=1)

        if now() - token_created_at > token_valid_duration:
            return render(request, "UserManage/FindPassword/password_reset_invalid.html")

        if request.method == "POST":
            new_password = request.POST.get("new_password1")
            confirm_password = request.POST.get("new_password2")

            if new_password != confirm_password:
                return render(request, "UserManage/FindPassword/password_reset_confirm.html", {
                    "error": "비밀번호가 일치하지 않습니다.",
                    "uid": uidb64,
                    "token": token
                })

            user.set_password(new_password)
            user.save()

            # **사용 후 캐시에서 토큰 삭제**
            cache.delete(cache_key)

            return redirect("users:login")

        return render(request, "UserManage/FindPassword/password_reset_confirm.html", {"uid": uidb64, "token": token})

    except (User.DoesNotExist, ValueError, TypeError):
        return render(request, "UserManage/FindPassword/password_reset_invalid.html")


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

    # Google 로그아웃 처리
    if 'google_access_token' in request.session:
        return google_logout(request)

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

def google_logout(request):
    # Google 세션 관련 정보 제거
    if 'google_access_token' in request.session:
        access_token = request.session['google_access_token']
        revoke_url = f"https://oauth2.googleapis.com/revoke?token={access_token}"

        # 토큰 취소 요청
        requests.post(revoke_url)

        # 세션에서 Google 관련 정보 삭제
        del request.session['google_access_token']

    # 일반 로그아웃 처리
    request.session.flush()

    # Google 로그아웃 페이지로 리디렉션
    messages.success(request, "Google에서 로그아웃되었습니다.")
    return redirect('users:login')

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

import logging

logger = logging.getLogger(__name__)

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
        logger.error("네이버 로그인 실패: 액세스 토큰 없음")
        return redirect('/?error=token_error')   # 오류 처리

    # 사용자 정보 요청
    user_info_url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_info_url, headers=headers)
    user_info = user_response.json().get("response")

    # 네이버에서 받아온 사용자 정보 로그 출력
    logger.info(f"Naver User Info: {user_info}")

    # 사용자 정보 추출
    email = user_info.get("email")
    nickname = user_info.get("nickname")
    user_id = user_info.get("id")
    profile_image_url = user_info.get("profile_image", f"{settings.STATIC_URL}defaultimage/default-image.jpg")  # 기본값 설정

    # 로그로 프로필 이미지 확인
    logger.info(f"Naver Profile Image URL: {profile_image_url}")

    naver_email = email.split('@')[0]+'@naver.com'

    try:
        # 기존 유저 확인
        user = CustomUser.objects.get(email=naver_email)
        user.profile_image_url = profile_image_url  # 프로필 이미지 업데이트
        user.save()
        created = False
        logger.info(f"기존 사용자 로그인: {user.email} / 프로필 이미지 업데이트됨")
    except CustomUser.DoesNotExist:
        # 신규 사용자 생성
        user = CustomUser.objects.create(
            user_id=user_id,
            email=naver_email,
            nickname=nickname,
            profile_image=profile_image_url,  # 프로필 이미지 저장
            is_active=True,
        )
        created = True
        logger.info(f"신규 사용자 생성: {user.email} / 프로필 이미지 저장됨")

    # 로그인 처리
    login(request, user)
    logger.info(f"로그인 성공: {user.email}")

    # 성공 페이지 렌더링
    context = {
        "user": user,
        "created": created,
    }
    return render(request, "main/main(afterLogin).html", context)

def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

    # 항상 계정 선택 화면이 나타나도록 prompt=select_account 추가
    url = (
        f"{google_auth_url}?"
        f"response_type=code&"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"scope={scope}&"
        "prompt=select_account"
    )
    return redirect(url)


# 구글 로그인
def google_callback(request):
    code = request.GET.get('code')
    token_url = "https://oauth2.googleapis.com/token"
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    if not code:
        logger.error("Google 로그인 실패: 인증 코드 없음")
        return JsonResponse({'error': '인증 코드가 없습니다.'}, status=400)

    # 🔹 Access Token 요청
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        logger.error("Google 로그인 실패: Access Token 요청 실패")
        return JsonResponse({'error': 'Access Token 요청 실패'}, status=400)

    # 🔹 사용자 정보 가져오기
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # Google API 응답 로그 출력
    logger.info(f"Google User Info: {user_info}")

    # 🔹 Google API 응답에서 필요한 정보 추출
    google_id = user_info.get('id')  # Google 고유 사용자 ID
    name = user_info.get('name')
    email = user_info.get('email')  # 세션에 저장하거나 로그에 사용할 수 있음
    profile_image_url = user_info.get("picture", f"{settings.STATIC_URL}defaultimage/default-image.jpg")    # 프로필 이미지 기본값 설정


    logger.info(f"Google People API Response: {user_info}")
    # 프로필 이미지 로그 출력
    logger.info(f"Google Profile Image URL: {profile_image_url}")

    try:
        # 이메일이 기존 유저에 있으면 업데이트
        user = CustomUser.objects.get(email=email)
        user.profile_image_url = profile_image_url  # 기존 사용자 프로필 이미지 업데이트
        user.save()
        created = False
        logger.info(f"기존 사용자 로그인: {user.email} / 프로필 이미지 업데이트됨: {user.profile_image}")
    except CustomUser.DoesNotExist:
        # 이메일이 없으면 새로 생성
        user = CustomUser.objects.create(
            user_id=google_id,
            email=email,
            nickname=name,
            profile_image_url=profile_image_url,  # 프로필 이미지 저장
            is_active=True,
        )
        user.set_unusable_password()  # 구글 로그인 유저는 비밀번호 설정 X
        created = True
        logger.info(f"신규 사용자 생성: {user.email} / 프로필 이미지 저장됨")

    # 🔹 사용자 세션 로그인
    login(request, user)
    logger.info(f"로그인 성공: {user.email}")
    # 🔹 성공 페이지 렌더링
    context = {
        "user": user,
        "created": created,
    }
    return render(request, "main/main(afterLogin).html", context)

# 마이페이지
@login_required
def mypage_view(request):
    user_id = request.user.id  

    # 🔹 총 기록 조회 SQL 실행
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(id) AS total_records, 
                COALESCE(SUM(distance), 0) AS total_distance, 
                COALESCE(SUM(calories), 0) AS total_calories
            FROM record_detail
            WHERE user_id = %s;
        """, [user_id])
        row = cursor.fetchone()

    total_records = row[0] if row else 0
    total_distance = row[1] if row else 0
    total_calories = row[2] if row else 0

    # GET 요청에서도 form이 항상 존재하도록 초기화
    form = ProfileImageForm(instance=request.user)

    # 프로필 이미지 변경 처리
    if request.method == "POST" and "profile_image" in request.FILES:
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.profile_image_file = request.FILES["profile_image"]  # profile_image_file에 저장
            user.save()
            return redirect('users:mypage_view')

    context = {
        "user": request.user,
        "total_records": total_records,
        "total_distance": total_distance,
        "total_calories": total_calories,
        "form": form,  # form이 항상 context에 포함되도록 수정
    }
    return render(request, "UserManage/mypage.html", context)
