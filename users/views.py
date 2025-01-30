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

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        user = authenticate(request, user_id=user_id, password=password)  # 유저 인증

        if user is not None:
            login(request, user)
            return redirect('users:success')  # 로그인 성공 시 success.html로 이동
        else:
            return render(request, 'login.html', {'error': 'Invalid User ID or Password'})  # 로그인 실패

    return render(request, 'login.html')

def success_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')  # 로그인되지 않았다면 로그인 페이지로 리다이렉트

    return render(request, 'success.html', {'user': request.user})

User = get_user_model()

'''
회원가입 페이지 view
'''
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 입력받은 데이터 JSON 직렬화
            user_data = {
                'user_id': form.cleaned_data['user_id'],
                'email': form.cleaned_data['email'],
                'nickname': form.cleaned_data['nickname'],
                'password': form.cleaned_data['password1'],
            }
            encoded_data = urlsafe_base64_encode(force_bytes(json.dumps(user_data)))  # JSON 직렬화 후 인코딩

            # 이메일 인증 메일 발송
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            token = default_token_generator.make_token(User(email=user_data['email']))  # email만 있는 User 객체 사용

            message = render_to_string('activate_email.html', {
                'uid': encoded_data,  # JSON 직렬화된 데이터 사용
                'domain': current_site.domain,
                'token': token,
            })
            send_mail(
                mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [user_data['email']],
                fail_silently=False,
            )
            
            return HttpResponse('Please confirm your email address to complete the registration.')
    
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


'''
이메일 인증 view
'''
def activate(request, uidb64, token):
    try:
        # 저장된 유저 데이터 복호화
        decoded_data = force_str(urlsafe_base64_decode(uidb64))
        user_data = json.loads(decoded_data)  # JSON 디코딩

        # 토큰 검증
        temp_user = User(email=user_data['email'])  # email만 포함된 가짜 User 객체 생성
        if not default_token_generator.check_token(temp_user, token):
            return HttpResponse('Invalid activation link!')

        # 이메일 인증이 완료되었으므로 유저 계정 생성
        user = User.objects.create_user(
            user_id=user_data['user_id'],
            email=user_data['email'],
            password=user_data['password'],
            nickname=user_data['nickname'],
        )
        return HttpResponse('Thank you for your email confirmation. Now you can log in.')
    
    except Exception as e:
        return HttpResponse('Invalid activation link!')


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


    # 사용자 정보를 데이터베이스에 저장
    user, created = CustomUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            "email": email.split('@')[0]+'@naver.com',
            "nickname": nickname,
            "is_active": True,  # 네이버 로그인은 바로 활성화
        },
    )

    # 사용자 세션 로그인
    login(request, user)

    # success.html 렌더링
    context = {
        "user": user,  # user 객체를 템플릿에 전달
    }
    return render(request, "success.html", context)

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
    naver_email = email.split('@')[0]+'@naver.com'
    try:
        # 1️⃣ 이메일이 기존 유저에 있으면 그 유저로 로그인
        user = CustomUser.objects.get(email=naver_email)
        user.save()
        created = False

    except CustomUser.DoesNotExist:
        # 2️⃣ 이메일이 없으면 새로 생성
        user = CustomUser.objects.create(
            user_id=user_id,
            email=naver_email,
            nickname=nickname,
            is_active=True,  # 네이버 로그인은 바로 활성화
        )
        created = True

    # 3️⃣ 사용자 세션 로그인
    login(request, user)

    # 성공 페이지 렌더링
    context = {
        "user": user,
        "created": created,  # 새 유저인지 기존 유저인지 전달
    }
    return render(request, "success.html", context)

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
        return JsonResponse({'error': '인증 코드가 없습니다.'}, status=400)

    # Access Token 요청
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,  # 환경 변수에서 값 가져오기
        'client_secret': settings.GOOGLE_CLIENT_SECRET,  # 환경 변수에서 값 가져오기
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        return JsonResponse({'error': 'Access Token 요청 실패'}, status=400)

    # 사용자 정보 가져오기
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # Google API 응답에서 필요한 정보 추출
    google_id = user_info.get('id')  # Google 고유 사용자 ID
    name = user_info.get('name')
    email = user_info.get('email')  # 세션에 저장하거나 로그에 사용할 수 있음

    try:
        # 1️⃣ 이메일이 기존 유저에 있으면 그 유저로 로그인
        user = CustomUser.objects.get(email=email)
        user.save()
        created = False

    except CustomUser.DoesNotExist:
        # 2️⃣ 이메일이 없으면 새로 생성
        user = CustomUser.objects.create(
            user_id=google_id,
            email=email,
            nickname=name,
            is_active=True,
        )
        user.set_unusable_password()
        created = True

    # 3️⃣ 사용자 세션 로그인
    login(request, user)

    # 성공 페이지 렌더링
    context = {
        "user": user,
        "created": created,  # 새 유저인지 기존 유저인지 전달
    }
    return render(request, "success.html", context)

    # # 사용자 정보 저장 또는 기존 사용자 불러오기
    # user, created = CustomUser.objects.get_or_create(
    #     user_id=google_id,
    #     defaults={
    #         "email": email,
    #         "nickname": name,
    #         "is_active": True,  # 기본적으로 활성화
    #     }
    # )

    # if created:
    #     user.set_unusable_password()  # 소셜 로그인의 경우 비밀번호를 설정하지 않음
    #     user.save()

    # # 사용자 세션 로그인
    # login(request, user)

    # context = {
    #     "email": user.email,
    #     "nickname": user.nickname,
    #     "user_id": user.user_id,
    #     "date_joined": user.date_joined,
    #     "is_active": user.is_active,
    # }

    # return render(request, "success.html", context)
