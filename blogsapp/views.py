from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string

from blogsapp.models import Post

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

    return render(request, 'blogsapp/post_detail.html', context={'post': post})


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
