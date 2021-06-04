from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from blogsapp.models import Post, Comment

import json


def posts_list(request):
    posts = Post.objects.order_by('-created_at')

    return render(request, 'blogsapp/posts_list.html', context={'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # get_object_or_404 는 404 페이지를 표시할 때 사용하는 메소드로 무조건 적으로 404 페이지를
    # 표시해주는 것이 아니라 특정한 케이스에 없으면 404페이지를 띄우는 것이다.
    # 즉 데이터 처리하는 과정에서 해당 조건에 맞지 않으면 404 페이지를 띄우고 성공적으로 데이터 처리
    # 를 하게 되면 그에 맞는 기능을 수행 한다.

    comments = Comment.objects.filter(post=post_id)
    # 해당 글에 해당하는 댓글만 가져올 수 있도록 filter 로 각 post 에 해당하는 pk 값을 가져와서
    # 구분 지어 준다.

    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    # 기본적으로 상세 페이지에서 좋아요를 누를 수 있어야 한다.
    # 로그인 한 유저가 상세 페이지에서 좋아요를 눌렀으면 좋아요 취소 버튼이 나올 수 있게 구현을 해야한다.
    # 그렇기 때문에 맨처음에는 좋아요를 안 누른 상태이다 따라서 기본값은 False (is_liked = False) 로 설정 한다.
    # 그리고나서 조건문을 작성하는데 먼저 로그인 한 유저를 확인하기 위해 (id=request.user.id) 값으로 해당 유저의 pk 값을 가져 온다.
    # 그 다음 좋아요의 존재유무를 확인 하기 위해서 .exists() 메소드를 사용한다. 만약 해당 유저가 좋아요를 눌렀으면 Ture 이기 때문에
    # UI 상의 설정 상 좋아요 취소 구문이 나오게 된다.
    # 좋아요를 취소하면 유저가 좋아요한 데이터가 없기 때문에 다시 False 로 돌아 간다.

    return render(request, 'blogsapp/post_detail.html',
                  context={'post': post, 'comments': comments,  'is_liked': is_liked, 'total_likes': post.total_likes()})


@login_required
@require_POST
def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    is_liked = post.likes.filter(id=request.user.id).exists()

    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))


@login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()  # .strip 좌우 공백 제거
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력해주세요.')

        if not content:
            errors.append('내용을 입력해주세요.')

        if not errors:
            post = Post.objects.create(user=request.user, title=title, content=content, image=image)
            return redirect(reverse('post_detail', kwargs={'post_id': post.id}))
            # reverse 에서 kwargs 는 인수가 있는 URL 의 인수를 포함 시킬 때 사용한다.
            # kwargs 또는 args 둘 중 아무거나 사용해도 무방 하다.
            # 하지만 명시적으로 인자를 1개만 받을때는 args 여러개의 인자를 받을때는 kwargs 를 사용한다.

    return render(request, 'blogsapp/post_write.html', {'user': request.user, 'errors': errors})


@login_required
def comment_write(request):
    errors = []
    if request.method == 'POST':
        post_id = request.POST.get('post_id', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            errors.append("댓글을 입력해주세요.")

        if not errors:
            comment = Comment.objects.create(user=request.user, post_id=post_id, content=content)
            return redirect(reverse('post_detail', kwargs={'post_id': comment.post.id}))
        # kwargs={'post_id': comment.post.id} 에서 comment.post.id 는 comment 모델을 생각하면 된다 .
        # comment 모델을 보면 알 수 있듯이 comment 는 post 를 참조 하게 된다. 즉, 해당 comment 가 참조 하고 있는
        # post 의 pk 값과 현재 post 의 pk 값을 매핑 시키면서 맞으면 댓글을 생성하고 아니면 에러가 발생 한다.

    return render(request, 'blogsapp/post_detail.html', {'user': request.user, 'errors': errors})
