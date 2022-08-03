from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User, Follow
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

ELEMENT_QUANTITY = 10


def get_page(posts, request):
    paginator = Paginator(posts, ELEMENT_QUANTITY)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    post_list = Post.objects.select_related('group')
    page_obj = get_page(post_list, request)
    return render(request, 'posts/index.html', {'page_obj': page_obj})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = get_page(post_list, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = get_page(post_list, request)
    following = request.user.is_authenticated and (
        Follow.objects.filter(
            user=request.user,
            author=author,
        ).exists()
    )
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    post_comments = post.comments.all()
    context = {
        'post': post,
        'form': form,
        'comments': post_comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    name = request.user.username
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        form = form.save(commit=False)
        form.author_id = request.user.id
        form.save()
        return redirect('posts:profile', name)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect(
            'posts:post_detail',
            post_id=post_id
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {
            'form': form,
            'post_id': post_id,
            'is_edit': True
        })
    form.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = get_page(posts, request)
    is_follow = True
    context = {
        'page_obj': page_obj,
        'is_follow': is_follow,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:follow_index')


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(
        user=request.user,
        author__username=username
    ).delete()
    return redirect('posts:follow_index')
