from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Post, PostComment

# 게시글 목록 (페이지네이션 추가)
def together_main(request):
    posts = Post.objects.all().order_by('-created_at')  # 최신순 정렬
    paginator = Paginator(posts, 4)  # 한 페이지에 4개씩 표시

    page_number = request.GET.get('page')  # 현재 페이지 번호 가져오기
    page_obj = paginator.get_page(page_number)  # 페이지네이션 객체 생성

    return render(request, 'together/together_main.html', {'page_obj': page_obj})


# 게시글 상세 페이지
def together_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = PostComment.objects.filter(post=post).order_by('-created_at')  # 최신순 정렬

    return render(request, 'together/together_detail.html', {'post': post, 'comments': comments})


# 게시글 작성 페이지
@login_required
def together_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        picture = request.FILES.get('picture')  

        if not title or not content:
            return render(request, 'together/together_post.html', {'error': '제목과 내용을 입력해주세요.'})

        post = Post.objects.create(user=request.user, title=title, content=content, picture=picture)
        return redirect('post:together_detail', post_id=post.id)

    return render(request, 'together/together_post.html')


# 댓글 작성 기능 (AJAX 지원 추가)
@login_required
def together_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if not content:
            return JsonResponse({'success': False, 'error': '댓글 내용을 입력해주세요.'})

        comment = PostComment.objects.create(post=post, user=request.user, content=content)

        # AJAX 요청인 경우 JSON 응답 반환
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': '댓글이 등록되었습니다.', 'comment': comment.content})

        return redirect('post:together_detail', post_id=post.id)

    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})

@login_required
def together_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.user:  # 현재 로그인한 사용자가 글 작성자인 경우
        post.delete()
        return JsonResponse({'success': True})  # 성공하면 JSON 응답 반환
    else:
        return JsonResponse({'success': False, 'message': '삭제 권한이 없습니다.'})  # 실패 메시지 반환
