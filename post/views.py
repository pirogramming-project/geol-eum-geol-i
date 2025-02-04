from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment
from django.http import JsonResponse


def together_main(request):
    posts = Post.objects.all().order_by('-created_at')  # 최신순서로 정렬렬
    return render(request, 'together/together_main.html', {'posts': posts})


def together_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = PostComment.objects.filter(post=post).order_by('-created_at')  # 최신순서로 정렬렬
    return render(request, 'together/together_detail.html', {'post': post, 'comments': comments})


# 게시글 작성 페이지
@login_required
def together_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        picture = request.FILES.get('picture')  

        if title and content:
            post = Post.objects.create(user=request.user, title=title, content=content, picture=picture)
            return redirect('post:together_detail', post_id=post.id) 

    return render(request, 'together/together_post.html')


@login_required
def together_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)

        if content:
            comment = PostComment.objects.create(post=post, user=request.user, content=content)
            return redirect('post:together_detail', post_id=post.id) 
    
    return JsonResponse({'success': False, 'error': '댓글 내용을 입력해주세요.'})
